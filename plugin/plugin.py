from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Label import Label
from enigma import eTimer

from bitrate import Bitrate

class BitrateViewer(Screen):
	skin = """
		<screen position="200,300" size="350,160" zPosition="1" title="Bitrate viewer">
			<eLabel position="5,10" size="80,22" text="video" font="Regular;20" />
			<eLabel position="5,30" size="80,22" text="min" font="Regular;20" />
			<widget name="vmin" position="5,50" size="80,22" font="Regular;20" />
			<eLabel position="85,30" size="80,22" text="max" font="Regular;20" />
			<widget name="vmax" position="85,50" size="80,22" font="Regular;20" />
			<eLabel position="165,30" size="80,22" text="average" font="Regular;20" />
			<widget name="vavg" position="165,50" size="80,22" font="Regular;20" />
			<eLabel position="245,30" size="80,22" text="current" font="Regular;20" />
			<widget name="vcur" position="245,50" size="80,22" font="Regular;20" />
			<eLabel position="5,80" size="80,22" text="audio" font="Regular;20" />
			<eLabel position="5,100" size="80,22" text="min" font="Regular;20" />
			<widget name="amin" position="5,120" size="80,22" font="Regular;20" />
			<eLabel position="85,100" size="80,22" text="max" font="Regular;20" />
			<widget name="amax" position="85,120" size="80,22" font="Regular;20" />
			<eLabel position="165,100" size="80,22" text="average" font="Regular;20" />
			<widget name="aavg" position="165,120" size="80,22" font="Regular;20" />
			<eLabel position="245,100" size="80,22" text="current" font="Regular;20" />
			<widget name="acur" position="245,120" size="80,22" font="Regular;20" />
		</screen>""" 

	def __init__(self, session):
		Screen.__init__(self, session)

		self.startDelayTimer = eTimer()
		self.startDelayTimer.callback.append(self.bitrateAfterDelayStart)

		self.setTitle(_("Bitrate viewer"))
		self["vmin"] = Label("")
		self["vmax"] = Label("")
		self["vavg"] = Label("")
		self["vcur"] = Label("")
		self["amin"] = Label("")
		self["amax"] = Label("")
		self["aavg"] = Label("")
		self["acur"] = Label("")

		self["actions"] = ActionMap(["WizardActions"],
		{
			"back": self.keyCancel,
			"ok": self.keyCancel,
			"right": self.keyCancel,
			"left": self.keyCancel,
			"down": self.keyCancel,
			"up": self.keyCancel,
		}, -1)
		self.bitrate = Bitrate(session, self.refreshEvent, self.bitrateStopped)
		self.onLayoutFinish.append(self.__layoutFinished)

	def __layoutFinished(self):
		self.bitrateUpdateStart()

	def bitrateUpdateStart(self, delay=0):
		self.startDelayTimer.stop()
		self.startDelayTimer.start(delay, True)

	def bitrateAfterDelayStart(self):
		if not self.bitrateUpdateStatus():
			self.bitrate.start()

	def bitrateUpdateStatus(self):
		return self.bitrate.running

	def bitrateUpdateStop(self):
		self.startDelayTimer.stop()
		if self.bitrateUpdateStatus():
			self.bitrate.stop()

	def refreshEvent(self):
		self["vmin"].setText(str(self.bitrate.vmin))
		self["vmax"].setText(str(self.bitrate.vmax))
		self["vavg"].setText(str(self.bitrate.vavg))
		self["vcur"].setText(str(self.bitrate.vcur))
		self["amin"].setText(str(self.bitrate.amin))
		self["amax"].setText(str(self.bitrate.amax))
		self["aavg"].setText(str(self.bitrate.aavg))
		self["acur"].setText(str(self.bitrate.acur))

	def keyCancel(self):
		self.bitrate.stop()
		self.close()

	def bitrateStopped(self, retval):
		self.close()

def main(session, **kwargs):
	session.open(BitrateViewer)

def Plugins(**kwargs):
	desc = _("Show service's bitrate")
	text = _("BitrateViewer")
	return(PluginDescriptor(name=text, description=desc, where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main))
