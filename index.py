import urllib.request
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(usuario, programa, preco):
    msg = MIMEMultipart()
    message = (
        f"Plano café {programa} está disponível para a compra no valor de {preco}"
    )
    password = "fpfhocecpvnminbu"
    msg["From"] = "python.message.to.tasks@gmail.com"
    msg["To"] = usuario
    msg["Subject"] = "cafezinho"
    msg.attach(MIMEText(message, "plain"))
    server = smtplib.SMTP("smtp.gmail.com", port=587)
    server.starttls()
    server.login(msg["From"], password)
    server.sendmail(msg["From"], msg["To"], msg.as_string())
    server.quit()


def get_preco(page_text):
    s = page_text.find(">$") + 2
    e = page_text.find("<", s)
    preco = float(page_text[s:e])
    return preco


def is_ok_buy_coffe(preco, preco_to_buy):
    result = True if preco < preco_to_buy else False
    return result


def loop_to_get_right_preco(url, usuario, programa, max_preco):
    while True:
        coffe_site = urllib.request.urlopen(url)
        text = coffe_site.read().decode("utf8")
        coffe_preco = get_preco(text)
        print(f"\nPreço do café: ", coffe_preco)
        is_ok = is_ok_buy_coffe(coffe_preco, max_preco)
        if is_ok:
            send_email(usuario, programa, coffe_preco)
            print("\nBOM INVESTIMENTO\n")
        else:
            print("\nN VALE A PENA :( !!!!\n")
        time.sleep(900)


def have_number(input):
    for i in input:
        if i.isalpha():
            continue
        else:
            return True
    return False


def format_input_preco(input_preco):
    max_preco = []
    for i in input_preco:
        if i.isalpha():
            continue
        else:
            max_preco.append(i)
    max_preco = "".join(max_preco)
    max_preco = max_preco.replace(",", ".")
    return float(max_preco)


def main():
    user = input(
        "\nPara receber notificações sobre a compra do café\nEMAIL: "
    )
    case = "0"
    while case not in ["1", "2"]:
        case = input(
            "\nDigite o número de qual café você irá comprar.\n"
            + "\n 1: Café para todos clientes"
            + "\n 2: FIEIS DE VERDADE\n"
            + "\nSelecione: "
        )
    if case == "1":
        url = "http://beans.itcarlow.ie/precos.html"
        program = "NORMAL"
    else:
        url = "http://beans.itcarlow.ie/prices-loyalty.html"
        program = "FIEIS"

    while True:
        price_wanted = input("\nPreço máximo para à compra do café: ")
        if len(price_wanted) > 0 and have_number(price_wanted):
            max_price = format_input_preco(price_wanted)
            print("\nPreço máximo:", max_price)
            break

    awnser = ""
    while awnser not in ["s", "n"]:
        awnser = input("\nINICIAS LOOP? (s/n) ").lower()
    if awnser == "s":
        loop_to_get_right_preco(url, user, program, max_price)
    else:
        main()




if __name__ == "__main__":
    main()