from db_query import create_table,chung_last_ten,ulsan_last_ten,a_z_chung,a_z_ulsan,print_chung,print_ulsan


if __name__ == '__main__':
    choice = int(input('1.create // 2.start-to-end date // 3.last-10 row  : '))
    if choice == 1:
        create_table()
    elif choice ==2:
        where = input('Where?? ')
        start = input('start(eg:2021-04-25 18:00:00)')
        end   = input('end(eg:2021-04-25 19:00:00)')
        if where =='chung':
            a_z_chung(start,end)
        elif where =='ulsan':
            a_z_ulsan(start,end)
    elif choice ==3:
        where = input('query Where???')
        if where =='chung':
            chung_last_ten()
        elif where =='ulsan':
            ulsan_last_ten()
    elif choice ==4:
        where = input('Where?? ')
        if where =='chung':
            print_chung()
        elif where =='ulsan':
            print_ulsan()