from Username import Name
import Email_Scan
from webshot import web
from url import geturl
from portScan import port
from colorama import Fore, Style
from Email_Scan import GetEmail
from phonenum import number_scan
from ipmap import get_ip
import pyfiglet
import fontstyle


MainFunctions = {
    1: Name,
    2: number_scan,
    3: GetEmail,
    4: geturl,
    5: port,
    6: web,
    7: get_ip
}


def Menu():
    Selection = 1
    while True:
        text = pyfiglet.figlet_format("INFOSINT")
        ascii_banner = fontstyle.apply(text, 'bold')
        print(Fore.RED + ascii_banner )
        print(Style.RESET_ALL)
        print('')
        print("1. Username Scan")
        print("2. Phone Number")
        print("3. Email")
        print("4. URL Scan")
        print("5. Advance Port Scanner")
        print("6. Website Scraper")
        print("7. Ip Heatmap")
        print("8. Exit")
        print('')
        Selection = int(input(">> "))
        print('')
        if (Selection == 1):
            MainFunctions[Selection]()
        elif (Selection == 2):
            MainFunctions[Selection]()
        elif (Selection == 3):
            MainFunctions[Selection]()
        elif (Selection == 4):
            MainFunctions[Selection]()
        elif (Selection == 5):
            MainFunctions[Selection]()
        elif Selection == 6:
            MainFunctions[Selection]()
        elif Selection == 7:
            MainFunctions[Selection]()
        elif Selection == 8:
            exit()
        else:
            print("Please choose an Appropriate option")


if __name__ == "__main__":
    Menu()
