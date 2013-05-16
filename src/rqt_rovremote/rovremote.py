import os
import rospy

from qt_gui.plugin import Plugin
from python_qt_binding import loadUi
from python_qt_binding.QtGui import QWidget
from auv_msgs.msg import NavSts;
import numpy
import math

def wrapAngle(angle):
	if angle>math.pi:
		return angle - 2* math.pi;
	elif angle<-math.pi:
		return 2*math.pi + angle;
	else:
		return angle;

class RovRemotePlugin(Plugin):
	def _on_rovX_slider_changed(self):
		print 'rovX: ', self._widget.rovX.value()
		self._on_parameter_changed()

	def _on_rovY_slider_changed(self):
		print 'rovY: ', self._widget.rovY.value()
		self._on_parameter_changed()

	def _on_rovZ_slider_changed(self):
		print 'rovZ: ', self._widget.rovZ.value()
		self._on_parameter_changed()

	def _on_rovYaw_slider_changed(self):
		print 'rovYaw: ', wrapAngle((self._widget.rovYaw.value()+180)/180.0 * math.pi)/math.pi*180.0
		self._on_parameter_changed()
	
	def __init__(self, context):
		super(RovRemotePlugin, self).__init__(context)
		# Give QObjects reasonable names
		self.setObjectName('RovRemotePlugin')

		# Process standalone plugin command-line arguments
		from argparse import ArgumentParser
		parser = ArgumentParser()
		# Add argument(s) to the parser.
		parser.add_argument("-q", "--quiet", action="store_true",
		              dest="quiet",
		              help="Put plugin in silent mode")
		args, unknowns = parser.parse_known_args(context.argv())
		if not args.quiet:
		    print 'arguments: ', args
		    print 'unknowns: ', unknowns

		# Create QWidget
		self._widget = QWidget()
		# Get path to UI file which is a sibling of this file
		# in this example the .ui and .py file are in the same folder
		ui_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rovRemotePlugin.ui')
		# Extend the widget with all attributes and children from UI file
		loadUi(ui_file, self._widget)
		# Give QObjects reasonable names
		self._widget.setObjectName('RovRemotePluginUi')
		# Show _widget.windowTitle on left-top of each plugin (when 
		# it's set in _widget). This is useful when you open multiple 
		# plugins at once. Also if you open multiple instances of your 
		# plugin at once, these lines add number to make it easy to 
		# tell from pane to pane.
		if context.serial_number() > 1:
		    self._widget.setWindowTitle(self._widget.windowTitle() + (' (%d)' % context.serial_number()))
		# Add widget to the user interface
		context.add_widget(self._widget)
	
		#setup signals and slots
		self._widget.rovX.valueChanged.connect(self._on_rovX_slider_changed)
		self._widget.rovY.valueChanged.connect(self._on_rovY_slider_changed)
		self._widget.rovZ.valueChanged.connect(self._on_rovZ_slider_changed)
		self._widget.rovYaw.valueChanged.connect(self._on_rovYaw_slider_changed)

		# setup publishers
		#rospy.init_node("refgen");
		self._publisher = rospy.Publisher("rov/etaRef", NavSts);
		self._publisher = rospy.Publisher("rov/current", NavSts);

		#ref = NavSts();
		#self._publisher = None

	def _send_ref(self, x_linear,y_linear, z_linear, z_angular):
		print 'send ref'
		if self._publisher is None: 
			print 'not a publisher quit'			
			return
		ref = NavSts()
		ref.position.north  = x_linear
		ref.position.east   = y_linear
		ref.position.depth  = z_linear
		ref.orientation.yaw = z_angular
		print(ref)
		self._publisher.publish(ref)

	def _send_current(self, x_linear,y_linear, z_linear, z_angular):
		print 'send ref'
		if self._publisher is None: 
			print 'not a publisher quit'			
			return
		ref = NavSts()
		ref.position.north  = x_linear
		ref.position.east   = y_linear
		ref.position.depth  = z_linear
		ref.orientation.yaw = z_angular
		print(ref)
		self._publisher.publish(ref)


	def _on_parameter_changed(self):
		print 'parameter changed'
		self._send_ref(self._widget.rovX.value()/10.0,self._widget.rovY.value()/10.0,self._widget.rovZ.value()/10.0,wrapAngle((self._widget.rovYaw.value()+180)/180.0 * math.pi))

	def shutdown_plugin(self):
		# TODO unregister all publishers here
		pass
	def save_settings(self, plugin_settings, instance_settings):
		# TODO save intrinsic configuration, usually using:
		# instance_settings.set_value(k, v)
		pass

	def restore_settings(self, plugin_settings, instance_settings):
		# TODO restore intrinsic configuration, usually using:
		# v = instance_settings.value(k)
		pass

	#def trigger_configuration(self):
	# Comment in to signal that the plugin has a way to configure it
	# Usually used to open a configuration dialog

