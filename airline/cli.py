from . import api as repo
logged_in = False

def main_menu():
    print('\n' + '=' * 35)
    print('MAIN MENU'.center(30))
    print('=' * 35)
    print('1. Sign in')
    print('2. List upcoming flights')
    print('3. Search flights')
    print('4. Multi-criteria search')
    print('5. Show 10 cheapest flights')
    print('6. Flexible departures')
    print('7. Register')
    print('x. Exit')
    print('=' * 35)

def customer_menu():
    print('\n' + '=' * 35)
    print('CUSTOMER MENU'.center(30))
    print('=' * 35)
    print('1. List upcoming flights')
    print('2. Search flights')
    print('3. Multi-criteria flight search')
    print('4. Show 10 cheapest flights')
    print('5. Flexible departures')
    print('6. Purchase tickets')
    print('7. List upcoming tickets')
    print('8. Check in')
    print('0. Sign out')
    print('x. Exit')
    print('=' * 35)

def seller_menu():
    print('\n' + '=' * 35)
    print('SELLER MENU'.center(30))
    print('=' * 35)
    print('1. List upcoming flights')
    print('2. Search flights')
    print('3. Multi-criteria flight search')
    print('4. Show 10 cheapest flights')
    print('5. Flexible departures')
    print('6. Sell tickets')
    print('7. Check in')
    print('8. Edit ticket')
    print('9. Delete ticket')
    print('10. Search sold tickets')
    print('0. Sign out')
    print('x. Exit')
    print('=' * 35)

def manager_menu():
    print('\n' + '=' * 35)
    print('MANAGER MENU'.center(30))
    print('=' * 35)
    print('1. List upcoming flights')
    print('2. Search flights')
    print('3. Multi-criteria flight search')
    print('4. Show 10 cheapest flights')
    print('5. Flexible departures')
    print('6. Search sold tickets')
    print('7. Register sellers')
    print('8. Create flights')
    print('9. Edit flights')
    print('10. Manage ticket deletions')
    print('11. Reports')
    print('0. Sign out')
    print('x. Exit')
    print('=' * 35)

def main():
    global logged_in
    repo.load_all()
    while True:
        print()
        if not logged_in:
            main_menu()
        else:
            if repo.current_user[0][0] == 'customer':
                customer_menu()
            if repo.current_user[0][0] == 'seller':
                seller_menu()
            if repo.current_user[0][0] == 'manager':
                manager_menu()
        choice = input('>> ').lower()
        if choice == 'x':
            print('\nExiting the application. Thank you for using it!')
            break
        if not logged_in:
            if choice == '1':
                logged_in = repo.login()
            elif choice == '2':
                repo.list_upcoming_flights()
            elif choice == '3':
                repo.search_flights()
            elif choice == '4':
                repo.multi_criteria_search()
            elif choice == '5':
                repo.show_cheapest_flights()
            elif choice == '6':
                repo.flexible_departures()
            elif choice == '7':
                logged_in = repo.register_customer()
            else:
                print('Invalid option')
        elif choice == '0':
            print('\nSigned out successfully')
            repo.current_user.clear()
            logged_in = False
        elif choice == '1':
            repo.list_upcoming_flights()
        elif choice == '2':
            repo.search_flights()
        elif choice == '3':
            repo.multi_criteria_search()
        elif choice == '4':
            repo.show_cheapest_flights()
        elif choice == '5':
            repo.flexible_departures()
        elif choice == '6':
            if repo.current_user[0][0] == 'customer':
                repo.ticket_purchase_menu()
            elif repo.current_user[0][0] == 'seller':
                repo.sell_ticket()
            elif repo.current_user[0][0] == 'manager':
                repo.search_sold_tickets()
        elif choice == '7':
            if repo.current_user[0][0] == 'customer':
                repo.list_upcoming_tickets()
            elif repo.current_user[0][0] == 'seller':
                repo.seller_check_in()
            elif repo.current_user[0][0] == 'manager':
                repo.register_seller()
        elif choice == '8':
            if repo.current_user[0][0] == 'customer':
                repo.customer_check_in()
            elif repo.current_user[0][0] == 'seller':
                repo.edit_ticket()
            elif repo.current_user[0][0] == 'manager':
                repo.create_flight()
        elif choice == '9':
            if repo.current_user[0][0] == 'customer':
                print('Invalid option')
            elif repo.current_user[0][0] == 'seller':
                repo.delete_ticket()
            elif repo.current_user[0][0] == 'manager':
                repo.edit_flight()
        elif choice == '10':
            if repo.current_user[0][0] == 'customer':
                print('Invalid option')
            elif repo.current_user[0][0] == 'seller':
                repo.search_sold_tickets()
            elif repo.current_user[0][0] == 'manager':
                repo.manage_ticket_deletions()
        elif choice == '11':
            if repo.current_user[0][0] == 'customer':
                print('Invalid option')
            elif repo.current_user[0][0] == 'seller':
                print('Invalid option')
            elif repo.current_user[0][0] == 'manager':
                repo.reporting()
        else:
            print('Invalid option')
if __name__ == '__main__':
    main()
