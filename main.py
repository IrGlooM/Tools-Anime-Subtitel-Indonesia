import os
from scraaper import cari
from scraaper import riwayat

def clear_scree():
          os.system('cls' if os.name == 'nt' else 'clear')


def list_menu():
    print("="*40)
    print("      Tools Streaming Anime Indo")
    print("="*40)
    print("1.Search Anime")
    print("2.History")
    print("3.Exit")



def main():
      while True:
         try:
               clear_scree()
               list_menu()
               pilih_menu = int(input("\nMenu :"))

               if pilih_menu < 1 or pilih_menu > 3:
                       print("\nMenu Tidak Ada Di List")


               if pilih_menu == 1:
                             judul = input("\nJudul Anime :")
 
                             cari(judul)                            


               elif pilih_menu == 2:
                             riwayat()

               elif pilih_menu == 3:
                    exit()

                             
         except ValueError:
              print("\nInput Not Valid")



if __name__ == "__main__" :
        main()