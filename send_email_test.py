import smtplib,ssl
from gpiozero import LED
from gpiozero import MotionSensor
import smtplib, ssl
from picamera import PiCamera  
from time import sleep  
from email.mime.multipart import MIMEMultipart  
from email.mime.base import MIMEBase  
from email.mime.text import MIMEText  
from email.utils import formatdate  
from email import encoders  
  
camera = PiCamera()
camera.rotation = 180
camera.resolution = (1920, 1080)
#camera.framerate = 50
pir = MotionSensor(4)
  
#camera.start_preview()  
#sleep(5)  
#camera.capture('/home/pi/Desktop/image.jpg')     # image path set
#sleep(5)  
#camera.stop_preview()
    
def send_an_email():
    for i in range(8):
        sleep(0.5)
        camera.capture('/home/pi/Desktop/image%s.jpg' % i)
    
    toEmailAdd = 'to_email'
    myEmailAdd = 'your_email'
    subject = 'Photos from PiCamera'
        
    msg = MIMEMultipart('mixed')  
    msg['Subject'] = subject  
    msg['From'] = myEmailAdd  
    msg['To'] = toEmailAdd 
    msg.preamble = "This is a multi-part message in MIME format."   
    #msg.attach(MIMEText(text))  
  
    msgAlternative = MIMEMultipart('mixed')
    msg.attach(msgAlternative)

    msgText = MIMEText('This message is sent from Python. ')
    msgAlternative.attach(msgText)

    msgText = MIMEText('Sending Attachments', 'html')

    msgAlternative.attach(msgText)
    
    for i in range(8):
        fileName = "image" + str(i) + ".jpg"
        path = "/home/pi/Desktop/" + fileName;
        part = MIMEBase('application', "octet-stream")  
        part.set_payload(open(path, "rb").read())  
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename=%s' %fileName)   # File name and format name
        msg.attach(part)

  
    try:  
       s = smtplib.SMTP('smtp.gmail.com', 587)  # Protocol
       s.ehlo()  
       s.starttls()  
       s.ehlo()  
       s.login(user = 'your_email', password = 'your_password') 
       #s.send_message(msg)  
       s.sendmail(myEmailAdd, toEmailAdd, msg.as_string())  
       s.quit()  
    #except:  
    #   print ("Error: unable to send email")    
    except SMTPException as error:  
          print ("Error")        
  
while True:
    pir.wait_for_motion()
    print("Motion Detected")
    send_an_email()
    print("Sent email successfully")
    
    pir.wait_for_no_motion()
    print("Motion Stopped")
    
    sleep(180)
