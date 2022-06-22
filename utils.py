import hmac, hashlib, re

def sign(key, msg):
	return hmac.new( key.encode(), msg.encode(), hashlib.sha256 ).hexdigest()

def hasher(data):
	return hashlib.sha256(data.encode()).hexdigest()

def FormValidator(value, letype):
	if not value:
		return [f"● {letype} is not set."]
	value = value.strip()
	errors = []

	if letype == "email" and (not re.findall("^[A-Za-z0-9._]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,3}$", value) or len(value)>75):
		errors.append("Email format is not valid.")
		if len(value)>75:
			errors.append("Email too big.")
	if letype == "username" and (not re.findall("^[A-Za-z0-9-+._]+$", value) or len(value)<8 or len(value)>75):
		errors.append("Username: Minimum 8 characters, maximum 75, letters, digits and ./+/-/_ only.")
	if letype == "password" and (not re.findall("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", value) or len(value)<8 or len(value)>75):
		errors.append("Password: Minimum 8 characters, maximum 75, at least one letter and one number.")
	
	return ["● " + error for error in errors]
