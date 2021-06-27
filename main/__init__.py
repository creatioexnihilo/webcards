from flask import Flask,render_template,request,redirect,url_for,session
#for form
from form.form import FForm

#for filename of img
from werkzeug.utils import secure_filename
import os

from PIL import Image, ImageFont, ImageDraw , ImageOps, ImageFilter, ImageEnhance

import urllib.request


app = Flask(__name__)

#to put in dotenv???
app.config['SECRET_KEY']='okboomer'



@app.route("/")
def home():
	return render_template('home.html',home_a="active")

 
def text_align_right(width,font_width):
	x=width-10-font_width
	return x




#set upload folder for image
app.config["IMAGE_UPLOADS"] = "/upload"
#allowed extensions for img
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG"]
#max size
app.config["MAX_IMAGE_FILESIZE"] = 2024*2024*2024

#verify if img has . in it
def allowed_image(filename):
	if not "." in filename:
		return False
#verify if extension is valid
	ext = filename.rsplit(".", 1)[1]

	# #
	# session['img_ext']=ext

	print('allowed? '+ str(ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]))
	print(app.config["ALLOWED_IMAGE_EXTENSIONS"])
	if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
		return True
	else:
		return False
#verify if file size is allowed 
def allowed_image_filesize(filesize):
	if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
		return True
	else:
		return False

#form to complete
@app.route("/form", methods=["GET", "POST"])
def form():
	#form it's equal to the class form defined in form.py
	form=FForm()
	#check if method is post
	if request.method == "POST":
		if request.files:	
			print('"filesize" and "size_of_profile" in request.cookies:' +str("filesize" and "size_of_profile" in request.cookies))
			if "filesize" and "size_of_profile" in request.cookies:
				if not allowed_image_filesize(request.cookies["filesize"]):
					print("Filesize exceeded maximum limit")
					return redirect(request.url)
				#image it's equal to image name from form.html
				image = request.files["image"]

				profile = request.files["face_image"]
				

				#check if filename is empty
				if image.filename == "":
					print("No filename")
					return redirect(request.url)

				#check if image is allowed
				print("allowed_image(image.filename:)"+str(allowed_image(image.filename)))
				if allowed_image(image.filename):

					filename = secure_filename(image.filename)

					#gets color from imput name="color_pick"
					color_pick=request.values.get("color_pick")

					phone=request.values.get("phone")

					occupation=request.values.get("occupation")


					ext=filename.rsplit('.',1)[1]
					img_upload="upload."+ext



					#image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

					#save image in upload folder
					image.save(os.path.join(".","static","im","images","upload",img_upload))
					print("Image saved")

				else:
					return redirect(request.url)

				###########################
				#image profile
				#check if filename is empty
				if profile.filename == "":
					print("No filename")
					return redirect(request.url)

				#check if image is allowed

				print("allowed_image(profile.filename:)"+str(allowed_image(profile.filename)))
				if allowed_image(profile.filename):

					#get profile filename
					profile_face = secure_filename(profile.filename)


					ext=profile_face.rsplit('.',1)[1]
					profile_upload="profile."+ext



					#image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

					#save image in upload folder
					profile.save(os.path.join(".","static","im","images","upload",profile_upload))
					print("Profile Image saved")

				################################

					#save variables and transmit them throught the session
					session['filename'] = img_upload
					session['firstname']=form.firstname.data
					session['lastname']=form.lastname.data
					session['email']=form.email.data
					session['color_pick']=color_pick
					session['phone']=phone
					session['occupation']=occupation
					#added profile session for profile picture
					session['profile'] =profile_upload



					#return redirect(url_for("edit",filename=filename))

					#redirect to edit function
					return redirect(url_for("edit"))
				else:
					#redirect to request.url = redirect to the page that made the request = /form
					print("That file extension is not allowed")
					return redirect(request.url)
	return render_template("form.html",form=form)



@app.route("/edit")
def edit():
	

	#get variables from session
	filename = session['filename'] 
	first_name=session['firstname']
	last_name=session['lastname']
	email=session['email']
	color=session['color_pick']
	phone=session['phone']
	occupation=session['occupation']
	profile=session['profile']

	
	#get image from folder
	my_image = Image.open(os.path.join(".","static","im","images","upload",filename))
	#resize image
	my_image = my_image.resize((340,189))

	



	width, height = my_image.size
	#get font from folder
	title_font = ImageFont.truetype(os.path.join(".",'OpenSans-Regular.ttf'), 15)

	
	
	#create an image duplicate that is's editable
	image_editable = ImageDraw.Draw(my_image)
	#put the text on the image

	

	#create strings of text
	text_first_name = "First Name: "+ first_name
	text_last_name = "Last Name: "+ last_name
	text_email = "Email: "+ email
	text_phone = "Phone: "+ phone
	text_occupation = "Occupation: "+ occupation 
	###########################################


	max_font_width=0
	#get strings and position them after their width
	font_width = title_font.getsize(text_first_name)[0]
	image_editable.text((text_align_right(width,font_width),(height/2)-0.3*height),text_first_name, color, font=title_font)
	#check if max_font_width is less than actual font_width
	if max_font_width<font_width:
		max_font_width=font_width

	font_width = title_font.getsize(text_last_name)[0]
	image_editable.text((text_align_right(width,font_width),(height/2)-0.2*height),text_last_name, color, font=title_font)

	if max_font_width<font_width:
		max_font_width=font_width

	font_width = title_font.getsize(text_email)[0]
	image_editable.text((text_align_right(width,font_width),(height/2)-0.1*height),text_email, color, font=title_font)

	if max_font_width<font_width:
		max_font_width=font_width

	font_width = title_font.getsize(text_phone)[0]
	image_editable.text((text_align_right(width,font_width),(height/2)-0*height),text_phone, color, font=title_font)

	if max_font_width<font_width:
		max_font_width=font_width

	font_width = title_font.getsize(text_occupation)[0]
	image_editable.text((text_align_right(width,font_width),(height/2)+0.1*height),text_occupation, color,font=title_font)

	if max_font_width<font_width:
		max_font_width=font_width


	#get profile picture from file as "face"
	face = Image.open(os.path.join(".","static","im","images","upload",profile))
	
	
	


	#print('max_width '+str(max_font_width))

	#hardcoded value
	#resize face accordingly
	if max_font_width>198:
		#get the procent of width occupied by the longest text from total width-20
		k=max_font_width/(width-30)
		img_width_percent=1-k;
		face=face.resize((int(img_width_percent*width),int(img_width_percent*width)))
	else:
		face=face.resize((120,120))
	
	#print('face size '+str(face.size[0]) +' '+ str(face.size[1]))

	#make a bigger size
	smallsize=(face.size[0]*3,face.size[1]*3)
	#create a mask 
	mask=Image.new('L',smallsize,0)
	#draw mask
	draw=ImageDraw.Draw(mask)
	#draw ellipse
	draw.ellipse((0,0)+ smallsize, fill=255)
	#resize mask and add antialias
	mask=mask.resize(face.size,Image.ANTIALIAS)
	face.putalpha(mask)

	#paste face on the image
	my_image.paste(face, (10, int(height/2-0.4*height)), face)


	#save the image

	ext=filename.rsplit('.',1)[1]
	out="result."+ext
  
	

	

	my_image.save(os.path.join(".","static","im","images","result",out))
	print(str(width)+" "+str(height))
	
	

	# out="saved."+ext
	# urllib.request.urlretrieve(os.path.join(".","images","result",out), os.path.join(".","images","saved",out))
	print(out)

	return render_template("img.html",out=out)

@app.route('/about')
def about():
	return render_template("about.html",about_a="active")

@app.route('/contact')
def contact():
	return render_template("contact.html",contact_a="active")

if __name__== "__main__":
	#add host='0.0.0.0', to run on other devices
	app.run(host='0.0.0.0',debug=True)
