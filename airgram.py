#Author: gchavepeyer <geoffrey AT chavepeyer DOT be>
#Homepage : https://github.com/gchavepeyer/weechat-airgram
#  Derived a lot from :notifo
#   Author: ochameau <poirot.alex AT gmail DOT com>
#   Homepage: https://github.com/ochameau/weechat-notifo
#   Derived from: notify
#       Author: lavaramano <lavaramano AT gmail DOT com>
#       Improved by: BaSh - <bash.lnx AT gmail DOT com>
#       Ported to Weechat 0.3.0 by: Sharn - <sharntehnub AT gmail DOT com)
#   And from: notifo_notify
#       Author: SAEKI Yoshiyasu <laclef_yoshiyasu@yahoo.co.jp>
#       Homepage: http://bitbucket.org/laclefyoshi/weechat/
# This plugin send push notifications to your iPhone or Android smartphone
# by using airgramapp.com mobile application/services
# Requires Weechat 0.3.0
# Released under GNU GPL v2
#
import weechat, string, urllib, urllib2

weechat.register("airgram", "gchavepeyer", "0.1", "GPL", "airgram: Send push notifications to your iPhone/Android for pm and highlights.", "", "")

credentials = {
    "key" : "",
    "secret" : ""
#    "username": "",
#    "api_secret": ""
}

for option, default_value in credentials.items():
    if weechat.config_get_plugin(option) == "":
        weechat.prnt("", weechat.prefix("error") + "airgram: Please set option: %s" % option)
        weechat.prnt("", "airgram: /set plugins.var.python.airgram.%s STRING" % option)

# Hook privmsg/hilights
weechat.hook_print("", "irc_privmsg", "", 1, "airgram_show", "")

# Functions
def airgram_show(data, bufferp, uber_empty, tagsn, isdisplayed,
        ishilight, prefix, message):

    if (bufferp == weechat.current_buffer()):
        pass

    elif weechat.buffer_get_string(bufferp, "localvar_type") == "private":
        buffer = (weechat.buffer_get_string(bufferp, "short_name") or
                weechat.buffer_get_string(bufferp, "name"))
        show_notification("PM", prefix + ": " + message)

    elif ishilight == "1":
        buffer = (weechat.buffer_get_string(bufferp, "short_name") or
                weechat.buffer_get_string(bufferp, "name"))
        show_notification(buffer, prefix + ": " + message)

    return weechat.WEECHAT_RC_OK

def show_notification(chan, message):
    AIRGRAM_KEY = weechat.config_get_plugin("key")
    AIRGRAM_SECRET = weechat.config_get_plugin("secret")
    if AIRGRAM_KEY != "" and AIRGRAM_SECRET != "":
        url = "https://api.airgramapp.com/1/broadcast"
        opt_dict = {
            "msg": chan + ":" + message
            }
        opt = urllib.urlencode(opt_dict)
        basic = "Basic %s" % ":".join([AIRGRAM_KEY, AIRGRAM_SECRET]).encode("base64").strip()
        python2_bin = weechat.info_get("python2_bin", "") or "python"
        weechat.hook_process(
            python2_bin + " -c \"import urllib2\n"
            "req = urllib2.Request('" + url + "', '" + opt + "')\n"
            "req.add_header('Authorization', '" + basic + "')\n"
            "res = urllib2.urlopen(req)\n\"",
            30 * 1000, "", "")