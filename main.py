import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup, KeyboardButton, Contact
import random
from bson import ObjectId
from pymongo import MongoClient , UpdateOne
import time 

client = MongoClient("mongodb+srv://vivek1612prasad:dora1emon@cluster0.tfs7mpf.mongodb.net/?retryWrites=true&w=majority")
db = client["main_p2p"]

bot = telebot.TeleBot("6484492820:AAF8pz_Mf8xpVCTKXBke0a0lmp28m2WxW_k")
bot_info = bot.get_me()
user_states = {}
user_state = {}
user_data = {}
users_collection = db["users"]
admch = "-990854713 "
paych = "@P2PAdSSHOW"
admin_id = 1548793801


#admin part
@bot.message_handler(commands=['promote'])
def promote_to_admin(message):
    user_id = int(message.text.split(" ")[1])
    user = users_collection.find_one({"_id": message.chat.id})
    if user and user.get("admin") is True:
      userr = users_collection.find_one({"_id": user_id})
      if userr and userr.get("admin"):
        bot.send_message(message.chat.id, "User is already an admin.")
      else:
        users_collection.update_one({"_id": user_id}, {"$set": {"admin": True}})
        bot.send_message(message.chat.id, "User has been promoted to admin.")
    elif message.chat.id == admin_id:
      users_collection.update_one({"_id": admin_id}, {"$set": {"admin": True}})
    else:  
      bot.send_message(message.chat.id, "Only admins can use this command.")

@bot.message_handler(commands=['demote'])
def demote_from_admin(message):
    user_id = message.text.split(" ")[1]
    user = users_collection.find_one({"_id": message.chat.id})
    if user and user.get("admin") is True:
      userr = users_collection.find_one({"_id": int(user_id)})
      if userr and userr.get("admin") is True:
        users_collection.update_one({"_id": int(user_id)}, {"$set": {"admin": False}})
        bot.send_message(message.chat.id, "User has been demoted from admin.")
      else:
        bot.send_message(message.chat.id, "User is not an admin.")
    else:
      bot.send_message(message.chat.id, "Only admins can use this command.")


@bot.message_handler(commands=['ban'])
def ban_user(message):
    user_id = message.chat.id
    user = users_collection.find_one({"_id": user_id})
    if user and user.get("admin"):
        try:
            target_user_id = int(message.text.split("/ban ")[1])
            users_collection.update_one({"_id": target_user_id}, {"$set": {"banned": True}})
            bot.send_message(message.chat.id, f"User with ID {target_user_id} has been banned.")
        except IndexError:
            bot.send_message(message.chat.id, "Please provide a user ID to ban.")
        except ValueError:
            bot.send_message(message.chat.id, "Invalid user ID.")
    else:
        bot.send_message(message.chat.id, "Only admins can use this command.")


@bot.message_handler(commands=['unban'])
def unban_user(message):
    user_id = message.from_user.id
    user = users_collection.find_one({"_id": user_id})
    if user and user.get("admin"):
        try:
            target_user_id = int(message.text.split("/unban ")[1])
            users_collection.update_one({"_id": target_user_id}, {"$set": {"banned": False}})
            bot.send_message(message.chat.id, f"User with ID {target_user_id} has been unbanned.")
        except IndexError:
            bot.send_message(message.chat.id, "Please provide a user ID to unban.")
        except ValueError:
            bot.send_message(message.chat.id, "Invalid user ID.")
    else:
        bot.send_message(message.chat.id, "Only admins can use this command.")

@bot.message_handler(commands=['info'])
def info_message(message):
  user_id = message.from_user.id
  collection = db["orders"]
  if user_id:
    info = message.text.split("/info ")[1]
    user = users_collection.find_one({"_id": user_id})
    if user and user.get("admin"):
      data = collection.find({"uid": int(info)})
      for datas in data:
        if datas:
          collections = db["pay-method"]
          method_cursor= collections.find({"_id": ObjectId(datas['method'])})
          method = method_cursor[0]
          bot.send_message(message.chat.id, f"*📢 Type:* `{datas['type']}`\n*💸 {datas['type']}ing Amount: *`{datas['famo']}`\n*👉 {datas['type']}ing for: *`{datas['aamo']}`\n\n*1️⃣st Party User Details:-* \n\n  *    🆔User Id: *`{datas['user_id']}`\n  *    💼User Address: *`{method['method_details']}`\n  *    📝Transaction Id:* `{datas.get('tr_id')}`\n\n*2️⃣nd Party User Details:-*\n\n  *    🆔User Id: *`{datas.get('user_id2','None')}` \n      💼*User Address: *`{datas.get('user_adrs','None')}`\n\n*🤝 Admin Details:-* \n\n      🔐*Admin Id:* `{datas.get('admin','None')}`\n      🔐*Admin Address:* `{datas.get('admin_address','None')}`","markdown")        
    else: 
      bot.send_message(message.chat.id,"Admins Command")
  #except IndexError as e:
  else:
    bot.send_message(message.chat.id,"Kindly send in correct format\n\nFormat:- `/info <uid>`","markdown")

@bot.message_handler(commands=['panel'])
def panel_message(message):
  user_id = message.from_user.id
  user = users_collection.find_one({"_id": user_id})
  if user and user.get("admin"):
    bot.send_message(message.chat.id,"*Welcome To The Admin Panel\n\n🔹 Add Admin :-* `/promote <tg-id>`\n*🔹 Dismiss Admin :-* `/demote <tg-id>`\n*🔹 Ban User:-* `/ban <tg-id>`\n*🔹 Unban User:- *`/unban <tg-id>`\n*🔹 Broadcast :-* `/broadcast <your-message>`\n*🔹 Trade Information :-* `/info <trade-id>`\n🔹 *Admin List :- *`/list`","markdown")

@bot.message_handler(commands=['list'])
def list_message(message):
    user_id = message.from_user.id
    user = users_collection.find_one({"_id": user_id})
    if user and user.get("admin"):
      data = users_collection.find({"admin": True})
      list = ""
      for datas in data :
        list += f"`{datas['_id']}`\n"
      bot.send_message(message.chat.id,f"Admin Ids are Below\n\n{list}","markdown")

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = message.from_user.id
    user = users_collection.find_one({"_id": user_id})
    if user and user.get("admin"):
        try:
            broadcast_text = message.text.split("/broadcast ")[1]
            all_users = users_collection.find()
            sent_to_users = set()              
            for user in all_users:
                if not user.get("banned"):
                    if user["_id"] not in sent_to_users:
                        bot.send_message(user["_id"], broadcast_text)
                        sent_to_users.add(user["_id"])
            bot.send_message(message.chat.id, f"Broadcast sent to {len(sent_to_users)} users.")
        except IndexError:
            bot.send_message(message.chat.id, "Please provide a message to broadcast.")
    else:
        bot.send_message(message.chat.id, "Only admins can use this command.")



@bot.message_handler(commands=['start'])
def handle_start(message):
    dr = users_collection.find_one({"_id":message.chat.id})
    if dr and dr.get("banned"):
      bot.send_message(message.chat.id,"❌ You are banned ❌")
    else:
      collection = db['orders']
      collections = db['pay-method']
    
      params = message.text.split('/start ')
      if len(params) > 1:
        user = users_collection.find_one({"_id":message.chat.id}) 
        if user and user.get("contact") is None:
          bot.send_message(message.chat.id,"❌ Register Yourself in Bot First \n\n👉 Send /start")
        else:
          param = params[1]
          if param.startswith("order"):
            id = message.text.split('order')[1]
            data = list(collection.find({"uid": int(id)}))
            for datas in data:
              if(datas.get("status") == "hold"):
                bot.send_message(message.chat.id,"Another User is Currently Dealing \n\n⌛ You can Check Status After 5 Minutes")
              else:
                if datas.get('admin') is None:
                 bot.send_message(message.chat.id,"There is no admin Joined The deal \n\nKindly wait sometime then try again")
                elif datas.get("status") == "paid":
                  method = collections.find_one({"_id": ObjectId(datas['method'])})
                  keyboard = InlineKeyboardMarkup()
                  keyboard.row( InlineKeyboardButton("✅ Done", callback_data=f"/done {id}"))
                  collection.update_one({"uid": int(id)}, {"$set": {"status": "hold"}}, upsert=True)
                  bot.send_message(message.chat.id, f"🔹 *Kindly Pay To The Address Below\n\n💼 Address =* `{method['method_details']}`\n\n_⚠️ After Paying Click On ✅ Done_\n\n⌛ You Have only 5 minutes To pay",parse_mode="markdown",reply_markup=keyboard)
                  seconds = 5 * 60
                  time.sleep(seconds)
                  collection.update_one({"uid": int(id)}, {"$set": {"status": "paid"}}, upsert=True)
                else:
                  bot.send_message(message.chat.id,"Trade Closed")
          elif param.startswith("admin"):
            id = message.text.split('admin')[1]
            data = collection.find({"uid": int(id)})
            if data:
              for datas in data:
                if datas.get('admin') is None or datas.get("admin") == message.chat.id:
                  if datas.get("admin_address") is None:
                    bot.send_message(message.chat.id,"Kindly Send Your Currency Adress To recieve Assests.")
                    bot.register_next_step_handler(message, admin_address,id)
                  else:
                    bot.send_message(message.chat.id,"You Already Provided The Address")
                else:
                  bot.send_message(message.chat.id,"An Admin is Already Handelling The Deal")
            else:
              bot.send_message(message.chat.id,"Order Not Found")
      else:
        data = users_collection.find_one({"_id":message.chat.id})
        if data is not None:
          if data.get("name") is None:
           sent = bot.send_message(message.chat.id,"Kindly Enter Your Name .\n\n⚠️ Your Name Should Match Your Bank Account Details")
           user_state[message.chat.id] = sent.message_id
          elif data.get("contact") is None:
            keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            contact_button = KeyboardButton(text="📞 Share Contact", request_contact=True)
            keyboard.add(contact_button)
            sent_message = bot.send_message(message.chat.id, "Please share your contact 👇\n\n🔐 Your contact will not be Shared with Anyone.", reply_markup=keyboard)
            user_state[message.chat.id] = sent_message.message_id
          else:
            keyboard = InlineKeyboardMarkup()
            keyboard.row(
        InlineKeyboardButton("👥 Profile",callback_data="/profile"),
        InlineKeyboardButton("📞 Support",callback_data="/support")
      )
            keyboard.row(
        InlineKeyboardButton("📢 P2P Corner",callback_data="/p2p")
      )
            keyboard.row(
            InlineKeyboardButton("📊 Statistics", callback_data="/stats"),InlineKeyboardButton("📝 Payment Method",callback_data="/payment")
          )
            bot.send_message(message.chat.id, "Welcome To P2P Bot",reply_markup=keyboard)
        else:
          sent_message = bot.send_message(message.chat.id,"Kindly Enter Your Name .\n\n⚠️ Your Name Should Match Your Bank Account Details")
          user_state[message.chat.id] = sent_message.message_id

    @bot.message_handler(func=lambda message: True)
    def handle_name(message):
      user_id = message.from_user.id
      user_name = message.text
      users_collection.update_one({"_id": user_id}, {"$set": {"name": user_name}}, upsert=True)
      bot.delete_message(message.chat.id,user_state.get(message.chat.id))
      bot.delete_message(message.chat.id,message.id)
      
      keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
      contact_button = KeyboardButton(text="📞 Share Contact", request_contact=True)
      keyboard.add(contact_button)
      sent_message = bot.send_message(message.chat.id, "Please share your contact 👇\n\n🔐 Your contact will not be Shared with Anyone.", reply_markup=keyboard)
      user_state[message.chat.id] = sent_message.message_id

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
  data = users_collection.find_one({"_id":message.chat.id})
  if data.get("contact") is None:
    print("f")
    user_id = message.from_user.id
    contact = message.contact
    if contact.user_id != user_id:
      bot.send_message(user_id,"⚠️ Kindly Send The Contact From Provide Button")
      bot.delete_message(message.chat.id,message.id)
    else:
      users_collection.update_one({"_id": user_id}, {"$set": {"contact": contact.phone_number}}, upsert=True)
      keyboard = InlineKeyboardMarkup()
      keyboard.row(
        InlineKeyboardButton("👥 Profile",callback_data="/profile"),
        InlineKeyboardButton("📞 Support",callback_data="/support")
      )
      keyboard.row(
        InlineKeyboardButton("📢 P2P Corner",callback_data="/p2p")
      )
      keyboard.row(
            InlineKeyboardButton("📊 Statistics", callback_data="/stats"),InlineKeyboardButton("📝 Payment Method",callback_data="/payment")
          )
      bot.send_message(message.chat.id, "Welcome To P2P Bot",reply_markup=keyboard)
      bot.delete_message(message.chat.id,user_state.get(message.chat.id))
      bot.delete_message(message.chat.id,message.id)

@bot.callback_query_handler(func=lambda call:
call.data.startswith("/support"))
def handle_support(call):
  if call.message.chat.username is None: 
    bot.send_message(call.message.chat.id,"⚠️ Error:- Kindly Add a Username First in your Telegram Id")
  else:
    bot.send_message(call.message.chat.id,"📞 Kindly Enter Your Message")
    bot.register_next_step_handler(call.message, support_text)

def support_text(message):
  user = users_collection.find({"admin":True})
  total= users_collection.count_documents({"admin": True})
  keyboard = InlineKeyboardMarkup()
  keyboard.row(
    InlineKeyboardButton("🗣️ Reply",callback_data=f"/reply {message.chat.id}")
  )
  if message.chat.username is None: 
    bot.send_message(message.chat.id,"⚠️ Error:- Kindly Add a Username First in your Telegram Id")
  else:
    for users in user:
      bot.send_message(users["_id"],f"📢 New Support Message From user\n\n User Id:- `{message.chat.id}`\nMessage: {message.text}\n\n⚠️ This Message is transferred to {total} Admins including You",reply_markup=keyboard,parse_mode="markdown")
    bot.send_message(message.chat.id,"We got your Request ")

@bot.callback_query_handler(func=lambda call:
call.data.startswith("/profile"))
def handle_profile(call):
  collection = db["orders"]
  trade = collection.count_documents({"user_id":call.message.chat.id,"status":"completed"})
  atrade = collection.count_documents({"user_id":call.message.chat.id,"status":"active"})
  rtrade = collection.count_documents({"user_id":call.message.chat.id,"status":"refunded"})
  
  bot.send_message(call.message.chat.id,f"*👤 Name*:- `{call.message.chat.first_name}`\n*🆔 User Id*:- `{call.message.chat.id}`\n*💱 Total Trades*:- `{trade}`\n*☢️ Active Trades*:- `{atrade}`\n*🔄 Refunded Trades*:- `{rtrade}`","markdown")


@bot.callback_query_handler(func=lambda call:
call.data.startswith("/reply"))
def handle_reply(call):
  pr_id = call.data.split("/reply ")[1]
  user_id = call.message.chat.id
  user = users_collection.find({"_id":user_id,"admin":True})
  if user:
    bot.send_message(user_id,"Kindly Enter Message You want to convey")
    bot.register_next_step_handler(call.message,reply2,pr_id)
  else:
    bot.send_message(user_id,"You are not a admin")

def reply2(message,pr_id):
  keyboard = InlineKeyboardMarkup()
  keyboard.row(
    InlineKeyboardButton("🗣️ Reply",callback_data="/support")
  )
  bot.send_message(pr_id,f"🗣️ Reply From Admin\n\nReply:- {message.text}",reply_markup=keyboard,parse_mode="markdown")
  bot.send_message(message.chat.id,"✅ Success")
  
@bot.callback_query_handler(func=lambda call:
call.data.startswith("/stats"))
def handle_stats(call):
  bot.send_message(call.message.chat.id,f"📊 Bot Live Stats 📊\n\n💡 Total Users: {users_collection.count_documents({})} User(s)\n\n🤟 Codes Maker: @p2psellersupportbot")
        
@bot.callback_query_handler(func=lambda call:
call.data.startswith("/payment"))
def handle_deposit(call):
    user_id = call.message.chat.id
    collection = db["pay-method"]
    method_count = collection.count_documents({"user_id": user_id})

    if method_count == 0:
      keyboard = InlineKeyboardMarkup()
      keyboard.row(InlineKeyboardButton("Add Payment Method", callback_data="add_method"))
      bot.send_message(call.message.chat.id, "You don't have any payment method. Add one by clicking below button.", reply_markup=keyboard)
    else:
      methods = collection.find({"user_id": user_id})
      keyboard = InlineKeyboardMarkup()
      keyboard.row(InlineKeyboardButton("Add Payment Method", callback_data="add_method"))
      for method in methods:
        keyboard.row(InlineKeyboardButton(method["method_name"], callback_data=f"view_method:{method['_id']}"))
      bot.send_message(call.message.chat.id, "Select a payment method:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "add_method")

def add_method_callback(call):
     bot.delete_message(call.message.chat.id, call.message.id)
     sent = bot.send_message(call.message.chat.id, "Enter the method name:")
     user_state[call.message.chat.id] = sent.message_id 
     bot.register_next_step_handler(call.message, add_method_name)

def add_method_name(message):
    collection = db["pay-method"]
    bot.delete_message(message.chat.id, user_state[message.chat.id])
    method_name = message.text
    user_id = message.from_user.id
    existing_method = collection.find_one({"user_id": user_id, "method_name": method_name})
    bot.delete_message(message.chat.id, message.id)
    if existing_method:
      bot.send_message(message.chat.id, "You already own a method with this name.")
    else:
        sent = bot.send_message(message.chat.id, "Enter the method details:")
        user_state[message.chat.id] = sent.message_id
        bot.register_next_step_handler(message, add_method_details, method_name)

def add_method_details(message, method_name):
    collection = db["pay-method"]
    method_details = message.text
    user_id = message.from_user.id
    bot.delete_message(message.chat.id, user_state[message.chat.id])

    method = {
        "user_id": user_id,
        "method_name": method_name,
        "method_details": method_details
    }
    collection.insert_one(method)
    bot.delete_message(message.chat.id, message.id)
    bot.send_message(message.chat.id, "Your payment method has been added successfully.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("view_method"))
def view_method_callback(call):
    collection = db["pay-method"]
    method_id = call.data.split(":")[1]
    method = collection.find_one({"_id": ObjectId(str(method_id))})
    keyboard = InlineKeyboardMarkup()
    
    
    if method:
        keyboard.row(InlineKeyboardButton("Delete Payment Method", callback_data=f"delete_method:{str(method_id)}"))
        response = f"Method Name: {method['method_name']}\nMethod Details: {method['method_details']}"
    else:
        response = "Payment method not found."

    bot.send_message(call.message.chat.id, response,reply_markup=keyboard)
    bot.delete_message(call.message.chat.id, call.message.id)

@bot.callback_query_handler(func=lambda call:call.data.startswith("delete_method"))
def delete_method_callback(call):
  collection = db["pay-method"]
  method_id = call.data.split(":")[1]
  collection.delete_one({"_id": ObjectId(method_id)})
  bot.send_message(call.message.chat.id, "Payment method deleted successfully.")
  bot.delete_message(call.message.chat.id, call.message.id)

@bot.callback_query_handler(func=lambda call:
                              call.data.startswith("verify_method"))
def verify_method_callback(call):
    collection = db["pay-method"]
    method_id = call.data.split(":")[1]
    print(method_id)
    method = collection.find_one({"_id": ObjectId(str(method_id))})
    keyboard = InlineKeyboardMarkup()
    
    
    if method:
        keyboard.row(InlineKeyboardButton("✅ Confirm", callback_data=f"confirm_method:{str(method_id)}"))
        response = f"Method Name: {method['method_name']}\nMethod Details: {method['method_details']}"
    else:
        response = "Payment method not found."

    bot.send_message(call.message.chat.id, response,reply_markup=keyboard)
    bot.delete_message(call.message.chat.id, call.message.id)
@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_method"))
def confirm_method_callback(call):
    collection = db["orders"]
    id = call.data.split(":")[1]
    
    collection.update_one({"user_id": call.message.chat.id,"uid":user_data[call.message.chat.id]}, {"$set": {"method": id}})
    dat = collection.find({"user_id": call.message.chat.id, "uid": user_data[call.message.chat.id]})
    des =  "Pay" if dat[0]['type'] == "Buy" else "Receive"
    sent = bot.send_message(call.message.chat.id, f"*Kindly Enter The Amount You want To {des} For your desired Deal followed By Currency*\nExample:- `100 INR`", parse_mode="markdown")
    user_state[call.message.chat.id] = sent.message_id
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.register_next_step_handler(call.message, add_fiat)

def add_fiat(message):
    collection = db["orders"]
    collections = db["pay-method"]
    collection.update_one({"user_id": message.chat.id, "uid": user_data[message.chat.id]}, {"$set": {"aamo": message.text}})

    bot.delete_message(message.chat.id, user_state[message.chat.id])
    bot.delete_message(message.chat.id, message.id)
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("✅ Confirm", callback_data="/confirm"))
    keyboard.row(InlineKeyboardButton("❌ Cancel", callback_data="/cancel"))
    data_cursor = collection.find({"user_id": message.chat.id, "uid": user_data[message.chat.id]})
    data = data_cursor[0]  
    method_cursor = collections.find({"_id": ObjectId(data['method'])})
    method = method_cursor[0]  
    trade = collection.count_documents({"user_id": message.chat.id,"status":"completed"})

    bot.send_message(message.chat.id, f"🔎 *Kindly Confirm Your Details Below*\n\n👤 *Name* = `{message.chat.first_name}`\n*📝 Ad For* = `{data['type']}`\n🧾 *{data['type']}ing Assets* = `{data['famo']}`\n💲 *{data['type']}ing in* = `{data['aamo']}`\n*🗣️ Total Trades* = `{trade}`\n\n🏧 *Payment Method* :-\n*🔹 Method Name* = `{method['method_name']}`\n🔹 *Method Details* = `{method['method_details']}`", reply_markup=keyboard,parse_mode='markdown')

@bot.callback_query_handler(func=lambda call: call.data.startswith("/confirm"))
def confir_method_callback(call):
  bot.delete_message(call.message.chat.id, call.message.id)
  collection = db['orders']
  collections = db['pay-method']
  data_cursor = collection.find({"user_id": call.message.chat.id, "uid": user_data[call.message.chat.id]})
  data = data_cursor[0]  
  method_cursor = collections.find({"_id": ObjectId(data['method'])})
  method = method_cursor[0]  
  trade = collection.count_documents({"user_id": call.message.chat.id,"status":"completed"})
  akeyboard = InlineKeyboardMarkup()
  akeyboard.row(InlineKeyboardButton(f"🛒 Join {data['type']}er",url=f"https://t.me/{bot_info.username}?start=admin{user_data[call.message.chat.id]}"))
  bot.send_message(admch,f"*Admin Post *\n\n👤 *{data['type']}er Name* = `{call.message.chat.first_name}`\n*📝 Ad For* = `{data['type']}`\n🧾 *{data['type']}ing Assets* = `{data['famo']}`\n💲 *{data['type']}ing in* = `{data['aamo']}`\n*🗣️ Total Trades* = `{trade}`\n\n🏧 *Payment Method* :-\n*🔹 Method Name* = `{method['method_name']}`\n🔹 *Method Details* = `{method['method_details']}`\n⌛ *Status* :- `Active`", reply_markup=akeyboard,parse_mode='markdown')
  bot.send_message(call.message.chat.id,"*Ad Created Successfully*",parse_mode="markdown")


@bot.callback_query_handler(func=lambda call:
                              call.data.startswith("/cancel"))
def cancel_method_callback(call):
    collection = db['orders']
    bot.delete_message(call.message.chat.id, call.message.id)
    collection.delete_one({"user_id": call.message.chat.id,"uid":user_data[call.message.chat.id]})
    bot.send_message(call.message.chat.id,"*❌ Cancelled Option*",parse_mode="markdown")
    

def admin_address(message,id):
  bot.send_message(message.chat.id,"Adress Sended")
  collection = db['orders']
  data = collection.find({"uid":int(id)})
  keyboard = InlineKeyboardMarkup()
  keyboard.row(
    InlineKeyboardButton("✅ Confirm",callback_data=f"/aconfirm {id}")
  )
  for datas in data:
    collection.update_one({"uid": int(id)}, {"$set": {"admin_address": message.text, "admin": message.chat.id}})
    bot.send_message(datas['user_id'],f"Kindly Pay To The Below Address \n\n`{message.text}` \n\nAfter Paying Click on ✅ Confirm.",reply_markup=keyboard,parse_mode="markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith('/aconfirm'))
def handle_aconfirm_query(call):
  bot.delete_message(call.message.chat.id,call.message.id)
  id = call.data.split("/aconfirm ")[1]
  bot.send_message(call.message.chat.id,"Kindly Enter Your Transaction Id or Link")
  bot.register_next_step_handler(call.message,tr_id,id)

def tr_id(message,id):
  collection = db['orders']
  collection.update_one({"uid": int(id)}, {"$set":{"tr_id":message.text}})
  data = collection.find_one({"uid":int(id)})
  admin = data['admin']
  keyboard = InlineKeyboardMarkup()
  keyboard.row(
    InlineKeyboardButton("👍 Recieved",callback_data=f"/received {id} {message.chat.id}"),InlineKeyboardButton("👎 Not Recieved", callback_data=f"/received no {message.chat.id} {id}")
  )
  bot.send_message(admin,f"Order Id: `{id}`\nTransaction:- `{message.text}`\nKindly Check Your Account User have Marked The Payment Done","markdown",reply_markup=keyboard)
  bot.send_message(message.chat.id,"Kindly Wait Now")

@bot.callback_query_handler(func=lambda call: call.data.startswith('/received'))
def handle_recieved_query(call):
  bot.delete_message(call.message.chat.id,call.message.id)
  collection = db['orders']
  collections = db['pay-method']
  id = call.data.split("/received ")[1]
  idd = id.split(" ")
  if str(idd[0]) == str("no"):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
    InlineKeyboardButton("🔄 Retry",callback_data=f"/aconfirm {idd[2]}")
  )
    bot.send_message(idd[1],"Your Payment Not Recieved",reply_markup=keyboard)
  else:
    collection.update_one({"uid": int(idd[0])}, {"$set": {"status": "paid"}})
    data = collection.find_one({"uid": int(idd[0])})
    method = collections.find_one({"_id": ObjectId(data['method'])})  
    trade = collection.count_documents({"user_id": idd[1],"status":"completed"})
    skeyboard = InlineKeyboardMarkup()
    skeyboard.row(InlineKeyboardButton("🛒 Deal Now",url=f"https://t.me/{bot_info.username}?start=order{idd[0]}"))
    bot.send_message(paych,f"*New Ad Created *\n\n\n*📝 Ad For* = `{data['type']}`\n🧾 *{data['type']}ing Assets* = `{data['famo']}`\n💲 *{data['type']}ing in* = `{data['aamo']}`\n*🗣️ Total Trades* = `{trade}`\n\n🏧 *Payment Method* :-\n*🔹 Method Name* = `{method['method_name']}`\n🔹 *Method Details* = `{method['method_details']}`\n⌛ *Status* :- `Active`", reply_markup=skeyboard,parse_mode='markdown')
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
    InlineKeyboardButton("💱 Refund",callback_data=f"/refund {idd[0]} {call.message.chat.id} {idd[1]}")
  )
    bot.send_message(call.message.chat.id,f"Order Id: `{idd[0]}`\n\nKindly Be Online and Wait for 2nd Party To join You\n\nIf There is no further Conversation Occur Kindky Click on 💱 Refund",reply_markup=keyboard,parse_mode="markdown")


@bot.callback_query_handler(func=lambda call: call.data.startswith('/refund'))
def handle_refund_query(call):
  bot.delete_message(call.message.chat.id,call.message.id)
  idd = call.data.split("/refund ")[1]
  id = idd.split(" ")
  keyboard = InlineKeyboardMarkup()
  keyboard.row(
    InlineKeyboardButton("🤝 Recieve",callback_data=f"/take {id[0]} {id[1]}")
  )
  bot.send_message(id[2],"Sorry we are unable to Fullfill Your Requirements \n\nKindly Click Below Button To Get Your Sended Assets",reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('/take'))
def handle_take_query(call):
  bot.delete_message(call.message.chat.id,call.message.id)
  idd = call.data.split("/take ")[1]
  id = idd.split(" ")
  bot.send_message(call.message.chat.id,"kindly send Your address/Bank To get Refund")
  bot.register_next_step_handler(call.message,take,f"{id[0]} {id[1]}",call.message.chat.id)

def take(message,id,chat_id):
  idd = id.split(" ")
  collection = db["orders"]
  bot.send_message(chat_id,f"You will Recive Your Money Safely after some time\n\n🗣️ For further discussion You can Visit Support Section\n\nYour Order Id:- {idd[0]}")
  keyboard = InlineKeyboardMarkup()
  keyboard.row(
    InlineKeyboardButton("✅ Confirm",callback_data=f"/cdone {chat_id}")
  )
  bot.send_message(idd[1],f"Order Id: `{id}`\nUser Provided Address \n\n👉 Address:- `{message.text}`\n\nKindly Refund To him\n\n⚠️ After Paying Click on Confirm",reply_markup=keyboard,parse_mode="markdown")
  collection.update_one({"uid":int(idd[0])}, {"$set": {"status": "refunded"}}, upsert=True)

@bot.callback_query_handler(func=lambda call: call.data.startswith('/cdone'))
def handle_cdone_query(call):
  id = call.data.split("/cdone ")[1]
  bot.delete_message(call.message.chat.id,call.message.id)
  bot.send_message(id,"😊 Our Admins Has Paid You")
@bot.callback_query_handler(func=lambda call: call.data.startswith('/done'))
def handle_done_query(call):
  bot.delete_message(call.message.chat.id,call.message.id)
  collection = db['orders']
  id = call.data.split('/done ')[1]
  collection.update_one({"uid": int(id)}, {"$set": {"user_id2": call.message.chat.id}})
  bot.send_message(call.message.chat.id,"👉 Kindly Enter Your Details Where you want to recieve the Payment")
  bot.register_next_step_handler(call.message,user_adrs,id)


def user_adrs(message,id):
  collection = db['orders']
  collection.update_one({"uid": int(id)}, {"$set": {"user_adrs": message.text}})
  data = collection.find_one({
    "uid":int(id)
  })
  bot.send_message(message.chat.id,"Kindly Wait Now")
  keyboard = InlineKeyboardMarkup()
  keyboard.row(
    InlineKeyboardButton("👍 Recieved",callback_data=f"/ureceived {id}"),InlineKeyboardButton("👎 Not Recieved", callback_data=f"/ureceived no {id} {data['admin']}"))
  bot.send_message(data['user_id'],"Kindly Check Your Wallet \n\nAnd answer via the given Buttons",reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('/ureceived'))
def handle_ureceived_query(call):
  bot.delete_message(call.message.chat.id, call.message.id)
  collection = db['orders']
  idd = call.data.split('/ureceived ')[1]
  id = idd.split(" ")
  if str(id[0]) == str("no"):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
    InlineKeyboardButton("🔄 Retry",callback_data=f"/verify {id[1]} {id[2]}")
  )
    bot.send_message(id[2],"Your Payment Not Recieved\n\n⚠️ Kindly Pay & Climck on Retry",reply_markup=keyboard)
  else:
    data = collection.find({"uid":int(id[0])})
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
    InlineKeyboardButton("✅ Paid", callback_data=f"/paid {id[0]}")
  )
    for datas in data:
      admin = datas['admin']
      adress = datas["user_adrs"]
      bot.send_message(admin,f"order Id :- `{id[0]}`\n\nUser Marked The Payment Received\n\nKindly Release Assests on below address\n\n`{adress}`\n\nAfter Paying Click on ✅ Paid",reply_markup=keyboard,parse_mode="markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith('/paid'))
def handle_paid_query(call):
  bot.delete_message(call.message.chat.id, call.message.id)
  bot.send_message(call.message.chat.id,"Thanks for your attention")
  collection = db['orders']
  id = call.data.split('/paid ')[1]
  data = collection.find({"uid":int(id)})
  collection.update_one({"uid": int(id)}, {"$set": {"status": "completed"}})
  for datas in data:
    bot.send_message(datas['user_id2'],"Kindly Check Your Wallet Our Team Have Paid You \n\nThanks For using our service")
  
  
@bot.callback_query_handler(func=lambda call: call.data.startswith('/p2p'))
def handle_callback_query(call):
        dr = users_collection.find_one({"_id":call.message.chat.id})
        if dr.get("banned"):
          bot.send_message(call.message.chat.id,"❌ You are banned ❌")
        else:
          keyboard = InlineKeyboardMarkup()
          keyboard.row(
            InlineKeyboardButton("💶 Buy", callback_data="/order buy"),
            InlineKeyboardButton("💱 Sell", callback_data="/order sell")
        )
          keyboard.row(
            InlineKeyboardButton("➕ Create an Ad", callback_data="/order create_ad")
        )
          keyboard.row(
            InlineKeyboardButton("🧒 Your Ads", callback_data="/order your_ads")
        )
          bot.send_message(call.message.chat.id, "Welcome To P2P Corner\n\n🤝 Select One Option From Below", reply_markup=keyboard)
    
@bot.callback_query_handler(func=lambda call: call.data.startswith('/order '))
def handle_order_callback(call):
  collection = db['orders']
  collections = db['pay-method']
  bot.delete_message(call.message.chat.id, call.message.id)
  option = call.data.split('/order ')[1]
  if option == 'sell':
    datas = collection.find({"type": "Buy","status":"paid"})
    
    if collection.count_documents({"type": "Buy","status":"paid"}) == 0 :
      
      
      bot.send_message(call.message.chat.id,"🔎 No Ads Found")
    else:
      for data in datas:
        uid = data["uid"]
        method_cursor = collections.find_one({"_id": ObjectId(data['method'])})
        user = bot.get_chat(data['user_id'])
        trade = collection.count_documents({"user_id": data['user_id'],"status":"completed"})
        if method_cursor is None:
          print("no")
        else:
          message_text = (
            f"👤 *Name*: `{user.first_name}`\n"
            f"*📝 Ad For*: `{data['type']}`\n"
            f"🧾 *{data['type']}ing Assets*: `{data['famo']}`\n"
            f"💲 *{data['type']}ing in*: `{data['aamo']}`\n"
            f"*🗣️ Total Trades*: `{trade}`\n\n"
            f"🏧 *Payment Method*:\n"
            f"*🔹 Method Name*: `{method_cursor['method_name']}`\n"
            f"🔹 *Method Details*: `{method_cursor['method_details']}`"
        )
          keyboard = InlineKeyboardMarkup()
          keyboard.row(InlineKeyboardButton("💼 Sell Now", url=f"https://t.me/{bot_info.username}?start=order{uid}"))
          bot.send_message(call.message.chat.id, message_text, reply_markup=keyboard, parse_mode='markdown')


  elif option == 'buy':
    datas = collection.find({"type": "Sell","status":"paid"})
    
    if collection.count_documents({"type": "Sell","status":"paid"}) == 0 :
      
      
      bot.send_message(call.message.chat.id,"🔎 No Ads Found")
    else:
      for data in datas:
      
        uid = data["uid"]
        method_cursor = collections.find_one({"_id": ObjectId(data['method'])})
        user = bot.get_chat(data['user_id'])
        trade = collection.count_documents({"user_id": data['user_id'],"status":"completed"})
        if method_cursor is None:
          print("no")
        else:
          message_text = (
            f"👤 *Name*: `{user.first_name}`\n"
            f"*📝 Ad For*: `{data['type']}`\n"
            f"🧾 *{data['type']}ing Assets*: `{data['famo']}`\n"
            f"💲 *{data['type']}ing in*: `{data['aamo']}`\n"
            f"*🗣️ Total Trades*: `{trade}`\n\n"
            f"🏧 *Payment Method*:\n"
            f"*🔹 Method Name*: `{method_cursor['method_name']}`\n"
            f"🔹 *Method Details*: `{method_cursor['method_details']}`"
        )
          keyboard = InlineKeyboardMarkup()
          keyboard.row(InlineKeyboardButton("💼 Buy Now",url=f"https://t.me/{bot_info.username}?start=order{uid}"))
          bot.send_message(call.message.chat.id, message_text, reply_markup=keyboard, parse_mode='markdown')
  elif option == 'create_ad':
      keyboard = InlineKeyboardMarkup()
      keyboard.row(
            InlineKeyboardButton("💶 Buy", callback_data="/order2 buy"),InlineKeyboardButton("💱 Sell", callback_data="/order2 sell"))
      bot.send_message(call.message.chat.id, "What you Want To Do ?",reply_markup=keyboard)
  elif option == 'your_ads':
    collection = db['orders']
    collections = db['pay-method']
    datas = collection.find({"user_id": call.message.chat.id})
    if collection.count_documents({"user_id": call.message.chat.id}) == 0 :
      
      
      bot.send_message(call.message.chat.id,"🔎 No Ads Found")
    else:
      #keyboard = InlineKeyboardMarkup()
      #keyboard.row(InlineKeyboardButton("➖ Delete",callback_data="/delete")
      for data in datas:
        method_cursor = collections.find_one({"_id": ObjectId(data.get('method'))})
        if method_cursor:
          user = bot.get_chat(data['user_id'])
          trade = collection.count_documents({"user_id": data['user_id'],"status":"completed"})
        
          message_text = (
            f"👤 *Name*: `{user.first_name}`\n"
            f"*📝 Ad For*: `{data['type']}`\n"
            f"🧾 *{data['type']}ing Assets*: `{data['famo']}`\n"
            f"💲 *{data['type']}ing in*: `{data['aamo']}`\n"
            f"*🗣️ Total Trades*: `{trade}`\n\n"
            f"🏧 *Payment Method*:\n"
            f"*🔹 Method Name*: `{method_cursor['method_name']}`\n"
            f"🔹 *Method Details*: `{method_cursor['method_details']}`")
          delete_button = InlineKeyboardButton("❌ Delete Ad", callback_data=f"delete_ad:{data['_id']}")
          keyboard = InlineKeyboardMarkup().add(delete_button)

          bot.send_message(call.message.chat.id, message_text, reply_markup=keyboard, parse_mode='markdown')
        


@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_ad:"))
def delete_ad_callback(call):
    collection = db['orders']
    ad_id = call.data.split(":")[1]
    collection.delete_one({"_id": ObjectId(ad_id)})
    bot.delete_message(call.message.chat.id,call.message.id)
    bot.send_message(call.message.chat.id, "Ad deleted successfully.")


@bot.callback_query_handler(func=lambda call: call.data.startswith('/order2 '))
def handle_order2_callback(call):
    collection = db["orders"]
    bot.delete_message(call.message.chat.id, call.message.id)
    option = call.data.split('/order2 ')[1]
    rand = random.randrange(10**9, 10**10)
    des =  "Buy" if option == "buy" else "Sell"
    inserts = {
   "user_id": call.message.chat.id,
   "type": des,
      "uid":rand
    }
    collection.insert_one(inserts)
    sent_message = bot.send_message(call.message.chat.id,"Kindly Send Your Amount followed by Coin Name \n\nExample :- `1 Usdt`",parse_mode="markdown")
    user_states[call.message.chat.id] = "WAITING_AMOUNT"
    user_state[call.message.chat.id] = sent_message.message_id
    user_data[call.message.chat.id] = rand
    
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "WAITING_AMOUNT")
def amount_handler(message):
  collection = db["pay-method"]
  collections = db["orders"]
  user_id = message.from_user.id
  collections.update_one({"user_id": user_id,"uid":user_data[user_id]}, {"$set": {"famo": message.text}})
           
  method_count = collection.count_documents({"user_id": user_id})
  bot.delete_message(message.chat.id,user_state.get(message.chat.id))
  bot.delete_message(message.chat.id,message.id)
  print(method_count)
  if method_count == 0:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton("Add Payment Method", callback_data="add_method"))
        bot.send_message(message.chat.id, "You don't have any payment method. Add one by clicking below button.", reply_markup=keyboard)
  else:
    methods = collection.find({"user_id": user_id})
    keyboard = InlineKeyboardMarkup()
    

    for method in methods:
          
          keyboard.row(InlineKeyboardButton(method["method_name"], callback_data=f"confirm_method:{method['_id']}"))
    bot.send_message(message.chat.id, "Select a payment method:", reply_markup=keyboard)
  user_states[message.chat.id] = "STARTED"
bot.infinity_polling(
  print("bot lanuched ...")
)
