import firebase
import firebase as my_firebase

c = my_firebase.connect()
# a = my_firebase.get_user_tokens(c)
my_firebase.send_notification(c, "Automated Garden", "Irrigação ligada...")
# my_firebase.send_notification2("Teste", "Mensagemmmm...... ")
# for key in a:
#     print(key)
# print(a)
# my_firebase.send_notification(
#     # "eOxApgg-R2mNrd5m8CMEb5:APA91bEGpYfkHYtK5YeUCqE5w357EoREdpUtwyxDu7UJ-Itk2YcRlXrc0PCQV6neZ2enUyQOcnYK5WAwaPm19_SBk0lXiDaBGKIzqdFYqZh-colhl0rM36j1msNWfCltftUCkk491k_K",
#     a,
#     "aaaa",
#     "bbbb"
# )
# print(a)