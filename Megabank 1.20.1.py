import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk
import json

f = open("myfile.json", "w")

class BankSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("سیستم مدیریت بانک")

        self.accounts = {}
        self.transactions = []

        self.root.geometry("800x500")

        self.welcome_label = tk.Label(root, text="به سیستم مدیریت بانک خوش آمدید!", font=("Helvetica", 16))
        self.welcome_label.pack()

        self.progress_bar = ttk.Progressbar(root, length=400, mode="indeterminate")
        self.progress_bar.pack()
        self.progress_bar.start()

        self.root.after(3000, self.show_login_page)

    def show_login_page(self):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()


                                                                        
        self.login_label = tk.Label(self.root, text="لطفاً یکی از گزینه‌های زیر را انتخاب کنید:")
        self.login_label.pack()

        self.register_button = tk.Button(self.root, text="ثبت نام", command=self.register_account)
        self.register_button.pack()

        self.login_button = tk.Button(self.root, text="ورود", command=self.login)
        self.login_button.pack()

    def register_account(self):
        name = simpledialog.askstring("ثبت نام", "نام:")
        if name:
            national_code = simpledialog.askstring("ثبت نام", "کد ملی:")
            if national_code:
                account_number = simpledialog.askstring("ثبت نام", "شماره حساب:")
                if account_number:
                    if account_number not in self.accounts:
                        password = simpledialog.askstring("ثبت نام", "رمز عبور:")
                        if password:
                            self.accounts[account_number] = {
                                "name": name,
                                "national_code": national_code,
                                "password": password,
                                "balance": 0,
                                "loan": 0,
                                "transactions": []
                            }
                            messagebox.showinfo("ثبت نام", "ثبت نام با موفقیت انجام شد.")
                        else:
                            messagebox.showerror("خطا", "لطفاً رمز عبور را وارد کنید.")
                    else:
                        messagebox.showerror("خطا", "این شماره حساب قبلاً ثبت شده است.")
                else:
                    messagebox.showerror("خطا", "لطفاً شماره حساب را وارد کنید.")
            else:
                messagebox.showerror("خطا", "لطفاً کد ملی را وارد کنید.")
        else:
            messagebox.showerror("خطا", "لطفاً نام را وارد کنید.")

    def login(self):
        account_number = simpledialog.askstring("ورود", "شماره حساب:")
        if account_number and account_number in self.accounts:
            password = simpledialog.askstring("ورود", "رمز عبور:")
            if password == self.accounts[account_number]["password"]:
                self.show_account_page(account_number)
            else:
                messagebox.showerror("خطا", "رمز عبور اشتباه است.")
        else:
            messagebox.showerror("خطا", "شماره حساب وارد شده یافت نشد.")

    def show_account_page(self, account_number):
        self.root.geometry("1000x600")
        self.root.title(f"سیستم مدیریت بانک - حساب {account_number}")

        account = self.accounts[account_number]

        self.account_label = tk.Label(self.root, text=f"نام: {account['name']} - موجودی: {account['balance']} - وام: {account['loan']}")
        self.account_label.pack()

        self.action_frame = tk.Frame(self.root)
        self.action_frame.pack()

        self.withdraw_button = tk.Button(self.action_frame, text="برداشت وجه", command=lambda: self.perform_transaction(account_number, "withdraw"))
        self.withdraw_button.grid(row=0, column=0, padx=10)

        self.deposit_button = tk.Button(self.action_frame, text="واریز وجه", command=lambda: self.perform_transaction(account_number, "deposit"))
        self.deposit_button.grid(row=0, column=1, padx=10)

        self.transfer_button = tk.Button(self.action_frame, text="انتقال وجه", command=lambda: self.perform_transaction(account_number, "transfer"))
        self.transfer_button.grid(row=0, column=2, padx=10)

        self.loan_button = tk.Button(self.action_frame, text="درخواست وام", command=lambda: self.request_loan(account_number))
        self.loan_button.grid(row=0, column=3, padx=10)

        self.history_button = tk.Button(self.action_frame, text="تاریخچه تراکنش‌ها", command=lambda: self.show_transaction_history(account_number))
        self.history_button.grid(row=0, column=4, padx=10)

    def perform_transaction(self, account_number, transaction_type):
        account = self.accounts[account_number]
        if transaction_type == "withdraw":
            amount = simpledialog.askinteger("برداشت وجه", "مبلغ را وارد کنید:")
            if amount and amount > 0 and amount <= account["balance"]:
                account["balance"] -= amount
                account["transactions"].append(f"برداشت وجه: {amount}")
                self.transactions.append(f"برداشت وجه از حساب {account_number}: {amount}")
                self.show_account_page(account_number)
            else:
                messagebox.showerror("خطا", "مبلغ وارد شده نامعتبر است یا موجودی کافی نیست.")
        elif transaction_type == "deposit":
            amount = simpledialog.askinteger("واریز وجه", "مبلغ را وارد کنید:")
            if amount and amount > 0:
                account["balance"] += amount
                account["transactions"].append(f"واریز وجه: {amount}")
                self.transactions.append(f"واریز وجه به حساب {account_number}: {amount}")
                self.show_account_page(account_number)
            else:
                messagebox.showerror("خطا", "مبلغ وارد شده نامعتبر است.")
        elif transaction_type == "transfer":
            recipient_account = simpledialog.askstring("انتقال وجه", "شماره حساب مقصد:")
            if recipient_account and recipient_account in self.accounts and recipient_account != account_number:
                amount = simpledialog.askinteger("انتقال وجه", "مبلغ را وارد کنید:")
                if amount and amount > 0 and amount <= account["balance"]:
                    account["balance"] -= amount
                    account["transactions"].append(f"انتقال وجه به شماره حساب {recipient_account}: {amount}")
                    self.accounts[recipient_account]["balance"] += amount
                    self.accounts[recipient_account]["transactions"].append(f"دریافت وجه از حساب {account_number}: {amount}")
                    self.transactions.append(f"انتقال وجه از حساب {account_number} به حساب {recipient_account}: {amount}")
                    self.show_account_page(account_number)
                else:
                    messagebox.showerror("خطا", "مبلغ وارد شده نامعتبر است یا موجودی کافی نیست.")
            else:
                messagebox.showerror("خطا", "شماره حساب مقصد نامعتبر یا مشابه شماره حساب فرستنده است.")

    def request_loan(self, account_number):
        account = self.accounts[account_number]
        if account["loan"] == 0:
            loan_amount = simpledialog.askinteger("درخواست وام", "مبلغ وام مورد نظر را وارد کنید:")
            if loan_amount and loan_amount > 0:
                account["loan"] = loan_amount
                account["balance"] += loan_amount
                account["transactions"].append(f"درخواست وام: {loan_amount}")
                self.transactions.append(f"درخواست وام به حساب {account_number}: {loan_amount}")
                self.show_account_page(account_number)
            else:
                messagebox.showerror("خطا", "مبلغ وارد شده نامعتبر است.")
        else:
            messagebox.showerror("خطا", "شما قبلاً وام گرفته‌اید.")

    def show_transaction_history(self, account_number):
        account = self.accounts[account_number]
        history_window = tk.Toplevel(self.root)
        history_window.title("تاریخچه تراکنش‌ها")

        history_label = tk.Label(history_window, text="تاریخچه تراکنش‌ها:")
        history_label.pack()

        history_text = tk.Text(history_window, wrap="word", height=15, width=60)
        history_text.pack()

        for transaction in account["transactions"]:
            history_text.insert("end", transaction + "\n")
        
        history_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankSystemApp(root)
    root.mainloop()
