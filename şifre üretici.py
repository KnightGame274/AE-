import random
import string

def sifre_olusturucu():
    uzunluk = int(input("Şifre uzunluğunu girin: "))
    karakterler = string.ascii_letters + string.digits + string.punctuation
    sifre = "".join(random.choice(karakterler) for _ in range(uzunluk))
    print(f"Oluşturulan Şifre: {sifre}")

sifre_olusturucu()