# import the necessary packages
from twilio.rest import Client
import boto3
from threading import Thread
import os

class TwilioNotifier:
	def __init__(self, conf):
		# store the configuration object
		self.conf = conf

	def send(self, msg, tempVideo):
		# start a thread to upload the file and send it
		t1 = Thread(target=self._send, args=(msg, tempVideo,"a"))
		t1.start()

	def send_path(self,msg,tempVideo,tempVideopath):
		# start a thread to upload the file and send it
		t2 = Thread(target=self._send, args=(msg, tempVideo,tempVideopath))
		t2.start()		

	def _send(self, msg, tempVideo,tempVideopath):
		# create a s3 client object
		s3 = boto3.client("s3",
			aws_access_key_id=self.conf["aws_access_key_id"],
			aws_secret_access_key=self.conf["aws_secret_access_key"],
		)

		# get the filename and upload the video in public read mode
		#filename = tempVideo
		#s3.upload_file("/home/mahesh/Downloads/pi-security-camera/"+tempVideo, self.conf["s3_bucket"],
		#	filename, ExtraArgs={"ACL": "public-read",
		#	"ContentType": "video/xvi"})
		if tempVideopath == "a":		
			filename = tempVideo
			s3.upload_file("/home/mahesh/Downloads/pi-security-camera/"+tempVideo, self.conf["s3_bucket"],
				filename, ExtraArgs={"ACL": "public-read",
				"ContentType": "video/xvi"})
			os.remove("/home/mahesh/Downloads/pi-security-camera/"+tempVideo)
		else:
			filename = tempVideo
			try:
				s3.upload_file(tempVideopath, self.conf["s3_bucket"],
				filename, ExtraArgs={"ACL": "public-read",
				"ContentType": "video/xvi"})
			except:
				print("Sepecified path not found :"+ tempVideopath)
		# get the bucket location and build the url
		location = s3.get_bucket_location(
			Bucket=self.conf["s3_bucket"])["LocationConstraint"]
		url = "https://s3-{}.amazonaws.com/{}/{}".format(location,
			self.conf["s3_bucket"], filename)
		print("Output file availabel at:" + url)
		#account_sid = 'ACc1411cf133899ab3f635e2aae15e5148'
		#auth_token = 'ec0b133f92b64fd399f06484671d7359'
		#client = Client(account_sid, auth_token)
		client = Client(self.conf["twilio_sid"], self.conf["twilio_auth"])
		message = client.messages.create(
				              body=msg+"\nDownload link:"+url,
				              #from_='+18508202151',
						from_ = self.conf["twilio_from"],to = self.conf["twilio_to"]
				              #to='+919762501815'
				          )

		print("Transaction ID:"+message.sid)
		print("File sent successfully..."+"\n"+"Now exiting")
