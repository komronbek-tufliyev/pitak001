import FCMManager as fcm

tokens = ['flTjs9aMTzyrZnuIgw4icO:APA91bE76wunMqQ441ai_LdT2ygCN0wsaZvMX7G2FbyU4FbvZsHnSP3YH2AQpDUriqo5XtUmZed8ZhtMMjmWYsPY3-zG7l9PE4CBiwfrGh02XYhtGLjz5_XQmljesszc0PwyxxhkxP-l', 'c44O3hjSQJqFlFDjoWzA3O:APA91bFvsc8Web4dlcbauhFPDnm_qWAgA5ev_zaqDoFTl3MOPl8SntULAK4Gq-k5yNsMZ0gnjcehDaJ321ftpzSBhfO8KFvXZyxe4kFwojUB__6sx2uysDkOmErDrzUil9rvvrc5VoEP']
fcm.send_push("hi", "This is a push message", tokens)