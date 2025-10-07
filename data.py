from telebot.types import (Message, CallbackQuery)
from typing import Union
from buttons import Buttons
from texts import texts
from database import get_user_lang
import re, os








def lang_msg(msg_obj: Union[Message, CallbackQuery], msg_key: str) -> str:
    lang = get_user_lang(msg_obj.from_user.id) or msg_obj.from_user.language_code or "en"
    return texts.get(msg_key, {}).get(lang, texts.get(msg_key, {}).get("en", ""))

def lang_buttons(msg_obj: Union[Message, CallbackQuery], buttons_key: str):
    lang = get_user_lang(msg_obj.from_user.id) or msg_obj.from_user.language_code or "en"
    return Buttons.get(buttons_key, {}).get(lang, Buttons.get(buttons_key, {}).get("en", []))


def checkPath(path):
	if os.path.exists(str(path)):
		return True;
	else:
		newD    = path.split('/');
		if newD[0] == '':
			if os.path.exists(str(newD[1])):
				os.system(f"touch {path}");
			else:
				os.system(f"mkdir /{newD[1]};touch {path} ");
		else:
			if os.path.exists(str(newD[0])):
				os.system(f"touch {path}");
			else:
				os.system(f"mkdir {newD[0]};touch {path}")

		return False;

def get(key,last_key=None,path='database/index.json'):
	key              = str(key);
	LK               = '';
	LKR             = LK;
	if last_key is not None:
		LK           = f"[{last_key}]";
		LKR         = "\["+last_key+"\]";
	
	checkPath(path);
	openDB   = open(str(path),'r');
	regEx       = "\n\["+key+"\]"+LKR+"=(.+)";
	content    = openDB.read();
	result        = re.findall(regEx,content);
	openDB.close();

	if result:
		return result[0];
	else:
		return False;


def se(key,last_key,option_value=None,path='database/index.json'):
	key              = str(key);
	LK               = '';
	value          = last_key;
	LKR             = LK;
	if option_value is not None:
		LK           = f"[{last_key}]";
		value      = option_value;
		LKR             = "\["+last_key+"\]";
		
	response  = False;
	checkPath(path);
	openDB   = open(str(path),'r');
	regEx       = "\n\["+key+"\]"+LKR+"=(.*)";
	content    = openDB.read();
	result        = re.findall(regEx,content);
	newV        = f"[{key}]{LK}={value}";
	DB             = open(str(path),'w');
	
	if result:
		newC        = content.replace(f"[{key}]{LK}={result[0]}",newV);
	else:
		content  += f"\n{newV}";
		newC       = content;
	try:
		DB.write(newC);
		response = True;
	except PermissionDenied:
		response = False;
	
	DB.close();
	openDB.close();
	
	return response;


def delete(key,last_key=None,path='database/index.json'):
	key              = str(key);
	response = True;
	LK               = '';
	LKR             = "(\[.*\])*"
	if last_key is not None:
		LK           = f"[{last_key}]";
		LKR         = "\["+last_key+"\]";
		
	
	checkPath(path);
	openDB   = open(str(path),'r');
	regEx       = "\n\["+key+"\]"+LKR+"=(.*)";
	content    = openDB.read();
	result        = re.findall(regEx,content);
	DB            = open(str(path),'w');
	
	if result:
		
		if LK == '':
			RMC    = LK;
			delL  = content;
			for iv in result:
				delL  = delL.replace(f"\n[{key}]{iv[0]}={iv[1]}",RMC);
			DB.write(delL);
			DB.close();
			
		else :
			RMC    = f"\n[{key}]{LK}=";
			delL  = content.replace(f"\n[{key}]{LK}={result[0]}",RMC);
			DB.write(delL);
	else:
		response =  False;
		DB.write(content);
	try:
		DB.close();
	except ValueError as nus:
		response = True;
	openDB.close();
	return response;
