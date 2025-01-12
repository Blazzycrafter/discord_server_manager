import time

from remoteauthclient import RemoteAuthClient
import segno
from PIL import Image
import asyncio

def getToken_QR(streamlit_app):
    st = streamlit_app
    st.write("please scan the QR code with your discord mobile app")

    c = RemoteAuthClient()

    @c.event("on_fingerprint")
    async def on_fingerprint(data):
        st.code(f"Fingerprint: {data.split('/')[-1]}")
        # make it bigger using next neighbor
        st.write(f"Generating QR code...")
        img = segno.make(data.split())
        img.save("qrcode.png")
        image = Image.open("qrcode.png")
        image = image.resize((300, 300), Image.NONE)
        st.image(image)

    @c.event("on_userdata")
    async def on_userdata(user):
        st.write(f"Username: {user.username}")
        st.write(f"Waiting for confirmation...")

    @c.event("on_token")
    async def on_token(token):
        st.write(f"Got Token...")
        #set token
        st.write(token)
        return token
    asyncio.run(c.run())