import csv

class BankingLogic:
    def __init__(self, ui):
        self.ui = ui
        self.accounts_file = "accounts.csv"
        self.current_account = None
        self.load_accounts()


        self.ui.Search_Button.clicked.connect(self.search_account)
        self.ui.Enter_pushButton.clicked.connect(self.process_transaction)
        self.ui.Exit_pushButton.clicked.connect(self.exit)
        self.ui.BuyBTC_pushButton.clicked.connect(self.buy_btc)
        self.ui.BuyETH_pushButton.clicked.connect(self.buy_eth)
        self.ui.BuyDOGE_pushButton.clicked.connect(self.buy_doge)
        self.ui.Withdraw_radioButton.setVisible(False)
        self.ui.Deposit_radioButton.setVisible(False)
        self.ui.Do_label.setVisible(False)
        self.ui.Amount_label.setVisible(False)
        self.ui.Amount_lineEdit.setVisible(False)
        self.ui.Exit_pushButton.setVisible(False)
        self.ui.Enter_pushButton.setVisible(False)

        self.ui.BuyCrypto_label.setVisible(False)
        self.ui.BTCPrice_label.setVisible(False)
        self.ui.ETHPrice_label.setVisible(False)
        self.ui.DOGEPrice_label.setVisible(False)
        self.ui.BTCAmount_lineEdit.setVisible(False)
        self.ui.BTC_label.setVisible(False)
        self.ui.BuyBTC_pushButton.setVisible(False)
        self.ui.ETHAmount_lineEdit.setVisible(False)
        self.ui.ETH_label.setVisible(False)
        self.ui.BuyETH_pushButton.setVisible(False)
        self.ui.DOGEAmount_lineEdit.setVisible(False)
        self.ui.DOGE_label.setVisible(False)
        self.ui.BuyDOGE_pushButton.setVisible(False)




    def load_accounts(self):
        self.accounts = []
        with open(self.accounts_file, 'r') as file:
            reader = csv.reader(file)

            next(reader)
            for row in reader:
                if len(row) == 4:
                    self.accounts.append({
                        'first_name': row[0],
                        'last_name': row[1],
                        'pin': row[2],
                        'balance': float(row[3])
                    })
                else:
                    print(f"Issue with row: {row}")

    def search_account(self):
        first_name = self.ui.FirstName_lineEdit.text()
        last_name = self.ui.LastName_lineEdit.text()
        pin = self.ui.PIN_lineEdit.text()

        for account in self.accounts:
            if (account['first_name'] == first_name and
                    account['last_name'] == last_name and
                    account['pin'] == pin):
                self.current_account = account
                self.ui.Welcome_label.setText(f"Welcome {first_name} {last_name}!")
                formatted_balance = f"{account['balance']:.2f}"
                self.ui.Results_label.setText(f"Current Balance: ${formatted_balance}")
                # Enable transaction options
                self.ui.Withdraw_radioButton.setVisible(True)
                self.ui.Deposit_radioButton.setVisible(True)
                self.ui.Do_label.setVisible(True)
                self.ui.Amount_label.setVisible(True)
                self.ui.Amount_lineEdit.setVisible(True)
                self.ui.Exit_pushButton.setVisible(True)
                self.ui.Enter_pushButton.setVisible(True)
                self.ui.Do_label.setEnabled(True)
                self.ui.Withdraw_radioButton.setEnabled(True)
                self.ui.Deposit_radioButton.setEnabled(True)

                self.ui.BuyCrypto_label.setVisible(True)
                self.ui.BTCPrice_label.setVisible(True)
                self.ui.ETHPrice_label.setVisible(True)
                self.ui.DOGEPrice_label.setVisible(True)
                self.ui.BTCAmount_lineEdit.setVisible(True)
                self.ui.BTC_label.setVisible(True)
                self.ui.BuyBTC_pushButton.setVisible(True)
                self.ui.ETHAmount_lineEdit.setVisible(True)
                self.ui.ETH_label.setVisible(True)
                self.ui.BuyETH_pushButton.setVisible(True)
                self.ui.DOGEAmount_lineEdit.setVisible(True)
                self.ui.DOGE_label.setVisible(True)
                self.ui.BuyDOGE_pushButton.setVisible(True)
                return

        # If account not found, display error message
        self.ui.Results_label.setText("Account not found. Please check your details.")

    def process_transaction(self):
        if self.current_account:
            amount = float(self.ui.Amount_lineEdit.text())
            if self.ui.Withdraw_radioButton.isChecked():
                if self.current_account['balance'] >= amount:
                    self.current_account['balance'] -= amount
                    self.ui.Results_label.setText(f"Withdrawal successful. New balance: ${self.current_account['balance']:.2f}")
                    self.save_balance()
                else:
                    self.ui.Results_label.setText("Insufficient balance.")
            elif self.ui.Deposit_radioButton.isChecked():
                self.current_account['balance'] += amount
                self.ui.Results_label.setText(f"Deposit successful. New balance: ${self.current_account['balance']:.2f}")
                self.save_balance()
        else:
            self.ui.Results_label.setText("Please search for an account first.")

    def save_balance(self):
        updated_accounts = []
        with open(self.accounts_file, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Skip the header row
            for row in reader:
                if (row[0] == self.current_account['first_name'] and
                        row[1] == self.current_account['last_name'] and
                        row[2] == self.current_account['pin']):
                    # Update the balance
                    row[3] = str(round(self.current_account['balance'], 2))
                updated_accounts.append(row)

        # Write updated accounts back to the file
        with open(self.accounts_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(updated_accounts)

    def buy_crypto(self, amount, crypto_price):
        total_cost = round(amount * crypto_price, 2)  # Round to 2 decimal places
        if self.current_account['balance'] >= total_cost:
            self.current_account['balance'] = round(self.current_account['balance'] - total_cost,
                                                    2)  # Deduct rounded amount
            self.ui.Results_label.setText(f"Purchase successful. New balance: ${self.current_account['balance']:.2f}")
            self.save_balance()
        else:
            self.ui.Results_label.setText("Insufficient balance.")

    def buy_btc(self):
        amount = float(self.ui.BTCAmount_lineEdit.text())
        btc_price = 60635  # Replace with actual BTC price
        self.buy_crypto(amount, btc_price)

    def buy_eth(self):
        amount = float(self.ui.ETHAmount_lineEdit.text())
        eth_price = 2989  # Replace with actual ETH price
        self.buy_crypto(amount, eth_price)

    def buy_doge(self):
        amount = float(self.ui.DOGEAmount_lineEdit.text())
        doge_price = 0.13  # Replace with actual DOGE price
        self.buy_crypto(amount, doge_price)


    def exit(self):
        # Close the application
        self.ui.close()