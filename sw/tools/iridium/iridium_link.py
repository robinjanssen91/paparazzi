#!/usr/bin/env python
from twisted.internet import gtk2reactor
gtk2reactor.install()

from iridium_protocol import IridiumProtocol
from twisted.internet.protocol import DatagramProtocol
from twisted.application import internet
from socket import SOL_SOCKET, SO_BROADCAST
import serial
import pygtk
import gtk
import os
pygtk.require('2.0')



DEFAULT_DEVICE = "/dev/paparazzi/iridium"
DEFAULT_BAUD = "19200"
DEFAULT_NUMBER = "00881111111111"
UDP_IN = 4243
UDP_OUT = 4242

# IridiumCtrl interface
class IridiumCtrl:

  def open(self, widget, data=None):
    try:
      self.serial = SerialPort(self.ir
        , self.entry_device.get_text(), reactor, baudrate=int(self.entry_baud.get_text()))
    except serial.SerialException as e:
      self.console_write("[ERROR] %s\r\n" % str(e))

  def cb_connected(self, val):
    self.lbl_connected.set_active(val)
    self.btn_open.set_sensitive(not val)

    self.btn_register.set_sensitive(val)
    self.btn_call.set_sensitive(val)
    self.btn_csq.set_sensitive(val)

  def cb_configured(self, val):
    self.lbl_configured.set_active(val)

    # Close it because it needs to be reconfigured
    if val == False and self.serial.connected:
      self.serial._serial.close()

  def cb_calling(self, val):
    self.lbl_in_call.set_active(val)
    self.btn_call.set_sensitive(not val)

    self.btn_register.set_sensitive(not val)
    self.btn_csq.set_sensitive(not val)

    if not val and self.lbl_redail.get_active():
      self.ir.call(self.entry_number.get_text())

  def cb_registered(self, val):
    self.lbl_registered.set_active(val)

  def cb_call_data(self, data):
    self.udp.sendData(data)

  def call(self, widget, data=None):
    self.ir.call(self.entry_number.get_text())

  def register(self, widget, data=None):
    self.ir.register()

  def csq(self, widget, data=None):
    self.ir.get_csq()

  def console_write(self, text):
    buf = self.console.get_buffer()
    buf.insert(buf.get_end_iter(), text)
    adj = self.sw_console.get_vadjustment()
    adj.set_value(adj.get_upper())

  def __init__(self):
    # Create the iridium device
    self.ir = IridiumProtocol(
      cb_connected = self.cb_connected,
      cb_configured = self.cb_configured,
      cb_calling = self.cb_calling,
      cb_registered = self.cb_registered,
      cb_call_data = self.cb_call_data)

    # Create the udp device
    self.udp = PprzUDPProtocol(in_port = UDP_IN, out_port = UDP_OUT, cb_recv_data = self.ir.transmit)
    reactor.listenUDP(UDP_IN, self.udp)

    # Create a new window
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.set_title("Iridium Link Controller")
    self.window.connect("destroy", self.destroy)
    self.window.set_default_size(600, 400)

    # Devide the window vertical
    self.vbox = gtk.VBox()
    self.window.add(self.vbox)

    # Create a split console overview
    self.hbox = gtk.HBox(spacing = 10)
    self.vbox.add(self.hbox)

    # Create a status window
    self.status_wind = gtk.VBox()
    self.status_wind.set_size_request(180,400)
    self.hbox.pack_start(self.status_wind, expand=False)
    #self.hbox.add(self.status_wind)

    # Setting - Device
    self.lbl_device = gtk.Label("Device")
    self.status_wind.add(self.lbl_device)
    self.entry_device = gtk.Entry()
    self.entry_device.set_text(DEFAULT_DEVICE)
    self.status_wind.add(self.entry_device)

    # Setting - Baud rate
    self.lbl_baud = gtk.Label("Baud rate")
    self.status_wind.add(self.lbl_baud)
    self.entry_baud = gtk.Entry()
    self.entry_baud.set_text(DEFAULT_BAUD)
    self.status_wind.add(self.entry_baud)

    # Setting - Phone number
    self.lbl_number = gtk.Label("Phone number")
    self.status_wind.add(self.lbl_number)
    self.entry_number = gtk.Entry()
    self.entry_number.set_text(DEFAULT_NUMBER)
    self.status_wind.add(self.entry_number)

    # Setting - Redail
    self.lbl_redail = gtk.CheckButton("Auto redail")
    self.status_wind.add(self.lbl_redail)

    # Status
    self.status_wind.add(gtk.HSeparator())
    self.lbl_connected = gtk.CheckButton("Connected")
    self.lbl_connected.set_sensitive(False)
    self.status_wind.add(self.lbl_connected)
    self.lbl_configured = gtk.CheckButton("Configured")
    self.lbl_configured.set_sensitive(False)
    self.status_wind.add(self.lbl_configured)
    self.lbl_registered = gtk.CheckButton("Registered")
    self.lbl_registered.set_sensitive(False)
    self.status_wind.add(self.lbl_registered)
    self.lbl_in_call = gtk.CheckButton("In call")
    self.lbl_in_call.set_sensitive(False)
    self.status_wind.add(self.lbl_in_call)

    # Add a console output
    self.sw_console = gtk.ScrolledWindow()
    self.sw_console.set_size_request(700,400)
    self.console = gtk.TextView()
    self.console.set_editable(False)
    self.ir.set_console(self.console_write)
    self.sw_console.add(self.console)
    self.hbox.add(self.sw_console)

    # Create a button toolbar
    self.toolbar = gtk.HBox()
    self.toolbar.set_size_request(0,40)
    self.vbox.pack_start(self.toolbar, expand=False)

    # Create the open device
    self.btn_open = gtk.Button("Open")
    self.btn_open.connect("clicked", self.open, None)
    self.toolbar.add(self.btn_open)

    # Create the reguster button
    self.btn_register = gtk.Button("Register")
    self.btn_register.connect("clicked", self.register, None)
    self.btn_register.set_sensitive(False)
    self.toolbar.add(self.btn_register)

    # Create the call button
    self.btn_call = gtk.Button("Call")
    self.btn_call.connect("clicked", self.call, None)
    self.btn_call.set_sensitive(False)
    self.toolbar.add(self.btn_call)

    # Create the CSQ button
    self.btn_csq = gtk.Button("CSQ")
    self.btn_csq.connect("clicked", self.csq, None)
    self.btn_csq.set_sensitive(False)
    self.toolbar.add(self.btn_csq)

    self.window.set_icon_from_file(os.getenv("PAPARAZZI_HOME") + "/sw/tools/iridium/sat.ico")

    # Show the window everything
    self.window.show_all()

  def destroy(self, widget, data=None):
    reactor.stop()

class PprzUDPProtocol(DatagramProtocol):
  cb_recv_data = False

  def __init__(self, in_port, out_port, cb_recv_data):
    self.port = in_port
    self.out_port = out_port
    self.cb_recv_data = cb_recv_data

  def startProtocol(self):
    self.transport.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, True)

  def sendData(self, data):
    self.transport.write(data, ('127.255.255.255', self.out_port))

  def datagramReceived(self, datagram, addr):
    if self.cb_recv_data != None:
      self.cb_recv_data(datagram)

if __name__ == "__main__":
  from twisted.internet import reactor
  from twisted.internet.serialport import SerialPort

  IridiumCtrl()
  reactor.run()
