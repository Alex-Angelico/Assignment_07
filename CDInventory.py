#------------------------------------------#
# Title: CDInventory.py
# Desc: Version of CD Inventory program
# incorporating binary storage and structured
# error handling.
# Change Log: (Who, When, What)
# Alex Angelico, 20200826, Created File
#------------------------------------------#

# -- DATA -- #
menuChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    
    @staticmethod
    def add_cd(ID, title, artist, table):
        """Collects new CD data from user and converts into dict for appending to current inventory table
        
        Args:
            ID (string): numerical identification for the new CD
            title (string): album title of the new CD
            artist (string): artist name of the new CD
            table (list of dicts): 2D data structure (list of dicts) that holds the data during runtime
        
        Returns:
            None.
        """
        dicRow = {'ID': ID, 'Title': title, 'Artist': artist}
        table.append(dicRow)
        print()
        
    @staticmethod
    def delete_cd(delID, table):
        """Deletes dicts by ID key from 2D data structure
        
        Args:
            delID (list of strings): holds one or more ID values designated for deletiton
            table (list of dicts): 2D data structure (list of dicts) that holds the data during runtime
            
        Returns:
            None.
        """
        remove_count = 0
        for row in delID: delID = row.strip().split(',')

        for _id in delID: # I do not know if it is possible complete a for loop after a nested except condition is triggered, but if it is I don't know how
            try:
                _id = int(_id)
            except:
                print('"',_id,'"',' is not valid ID input. Removing from delete list.', sep='')
                delID.remove(_id)
            pass
            for row in table:
                if row['ID'] == _id:
                    remove_count += 1
                    table.remove(row)

        if remove_count == 0: print('No matching IDs')
        else: print(f'{remove_count} total IDs removed out of {len(delID)}')

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()
        
        readcount = 0
        while readcount < 1:
            try:
                with open(file_name, 'rb') as fileObj:
                    data = pickle.load(fileObj)
                    readcount += 1
            except(IOError):
                print('CD Inventory file not found. Terminating program.')
                sys.exit()
            
        for line in data:
            try:
                if line != {}: table.append(line)
            except(TypeError, ValueError):
                print('Corrupt or missing data.')
                sys.exit()

    @staticmethod
    def write_file(file_name, table):
        """Function to manage transcription of data from list of dictionaries in
        current inventory to file
        
        Args:
            file_name (string): name of file used to wrtie the data to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
            
        Returns:
            None.
        """
        tempTbl = []
        FileProcessor.read_file(strFileName, tempTbl)
        savecount = 0
        while savecount < 1:
            try:
                if str(table) != str(tempTbl):
                    with open(file_name, 'wb') as objFile:
                        pickle.dump(table, objFile)
            except:
                print('There are no new CDs in Inventory to save.')
            savecount += 1

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        options = ['l', 'a', 'i', 'd', 's', 'x']
        while True:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
            try:
                if options.count(choice) == 1: break
            except:
                continue
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')
        
    @staticmethod
    # def add_cd_input(table, IDchecklist):
    def add_cd_input(table):
        """Gets user input for new CD information
        
        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.
        
        Returns:
            ID (string): numerical identification for the new CD
            title (string): album title of the new CD
            artist (string): artist name of the new CD
        """

        # We generate a list of all used ID's.
        used_ids = []
        for row in table:
            used_ids.append(row["ID"])

        # Prompt the user for an ID value
        while True:
            ID = input('Enter numerical ID: ').strip()
            try:
                ID = int(ID)
                break
            except:
                continue
        
        # If that ID value is currently in user, continue prompting.
        while ID in used_ids:
            print('That ID already exists. Please enter a new ID.')
            while True:
                ID = input('Enter numerical ID: ').strip()
                try:
                    ID = int(ID)
                    break
                except:
                    continue

        while True:
            title = input('What is the CD\'s title? ').strip()
            try:
                if (len(title)) > 0: break
            except:
                continue
        
        while True:
            artist = input('What is the Artist\'s name? ').strip()
            try:
                if (len(artist)) > 0: break
            except:
                continue

        return ID, title, artist

# 0. Import data storage and error handling modules
import pickle, sys

# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    menuChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if menuChoice == 'x':
        break
    # 3.2 process load inventory
    if menuChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        overwrite_verification = input('Type \'yes\' to continue and reload from file. Otherwise reload will be canceled.\n')
        if overwrite_verification.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif menuChoice == 'a':
        print("Please provide new CD info.")
        add_verification = 'y'
        while add_verification == 'y':
            # 3.3.1 Ask user for new ID, CD Title, and Artist
            cdID,cdTitle,cdArtist = IO.add_cd_input(lstTbl)
            # 3.3.2 Verify input data is correct
            print('\nYou entered:')
            print('ID\tCD Title (by: Artist)')
            print(f'{cdID}\t{cdTitle} (by:{cdArtist})\n')
            input_validation = input("Is this information correct? [y/n]: ").lower()
            if input_validation == "y":
                pass
            elif input_validation == "n":
                continue
            # 3.3.3 Add item to the table and ask user if they want to add another CD
            DataProcessor.add_cd(cdID, cdTitle, cdArtist, lstTbl)
            while True:
                add_verification = input('Would you like to add another CD? [y/n] ').lower()
                try:
                    if add_verification == 'y': break
                    elif add_verification == 'n': break
                except:
                    continue
        print()
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif menuChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif menuChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        while True:
            cdIDdel = [input('Enter one or more IDs to delete, separated by commas (example: "1,2,3"): ').strip()]
            try:
                if cdIDdel != ['']: break
            except:
                continue
        # 3.5.2 search through table and delete CD
        DataProcessor.delete_cd(cdIDdel, lstTbl)
        # 3.5.3 display altered Inventory to user
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif menuChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        while True:
            save_verification = input('Save this inventory to file? [y/n] ').strip().lower()
            # 3.6.2 Process choice
            try:
                if save_verification == 'y':
                    # 3.6.2.1 save data
                    FileProcessor.write_file(strFileName, lstTbl)
                    break
                elif save_verification == 'n':
                    input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
                    break
            except:
                continue
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')