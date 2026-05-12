import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from src.core.processor import AlegraProcessor


class AlegraApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Alegra Automation Tool v1.0")
        self.geometry("600x400")
        ctk.set_appearance_mode("dark")

        self.selected_file = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.lbl_title = ctk.CTkLabel(
            self,
            text="Cargador de Comprobantes Alegra",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.lbl_title.grid(row=0, column=0, padx=20, pady=20)

        self.btn_select = ctk.CTkButton(
            self, text="Seleccionar Excel", command=self.select_file
        )
        self.btn_select.grid(row=1, column=0, padx=20, pady=10)

        self.lbl_file = ctk.CTkLabel(
            self, text="Ningún archivo seleccionado", font=ctk.CTkFont(size=12)
        )
        self.lbl_file.grid(row=2, column=0, padx=20, pady=5)

        self.txt_log = ctk.CTkTextbox(self)
        self.txt_log.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")

        self.btn_run = ctk.CTkButton(
            self,
            text="Iniciar Procesamiento",
            state="disabled",
            command=self.start_process_thread,
        )
        self.btn_run.grid(row=4, column=0, padx=20, pady=20)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if file_path:
            self.selected_file = file_path
            self.lbl_file.configure(text=f"Archivo: {file_path.split('/')[-1]}")
            self.btn_run.configure(state="normal")

    def log(self, message):
        self.txt_log.insert("end", f"{message}\n")
        self.txt_log.see("end")

    def start_process_thread(self):
        self.btn_run.configure(state="disabled")
        self.btn_select.configure(state="disabled")
        self.log("Iniciando proceso...")

        thread = threading.Thread(target=self.run_process, daemon=True)
        thread.start()

    def run_process(self):
        try:
            processor = AlegraProcessor(self.selected_file)
            processor.process_invoices()
            self.log("Proceso finalizado. Revisa logs/app.log para detalles.")
            messagebox.showinfo("Éxito", "El proceso ha terminado.")
        except Exception as e:
            self.log(f"Error crítico: {str(e)}")
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
        finally:
            self.btn_run.configure(state="normal")
            self.btn_select.configure(state="normal")
