from streamlink import Streamlink

session = Streamlink()
session.set_plugin_option('twitch','oauth_token','6e0lp5sm8szjzkuso7r9kr3y7nzh9f')
#session.set_plugin_option('twitch','client-id','df1trcokk8t1si5eloxe1lg1e0040f')
VOD = 148361448 #http://twitch.tv/videos/148361448

twitch_plugin = session.plugins['twitch']
streams = twitch_plugin("https://www.twitch.tv/videos/{}".format(VOD)).streams()

print(streams['worst'])
print('Opening stream...')
with streams['worst'].open() as fd:
    with open('out.ts','wb') as out:
        for i in range(0,50000):
            if i % 50 == 0:
                print("Downloaded {} kB".format(i))
            data = fd.read(1024)
            out.write(data)

