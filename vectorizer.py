import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys
import platform
from PIL import Image, ImageFilter
import subprocess
import tempfile
import shutil
from pathlib import Path

class VectorizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bild Vektorisierer")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Fenster in den Vordergrund bringen (macOS)
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        
        # Variablen
        self.selected_folder = tk.StringVar()
        self.threshold_value = tk.IntVar(value=128)
        self.progress_var = tk.DoubleVar()
        
        self.setup_ui()
        
        # Fenster zentrieren
        self.center_window()
        
    def center_window(self):
        """Zentriert das Fenster auf dem Bildschirm"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_ui(self):
        # Hauptframe
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Titel
        title_label = ttk.Label(main_frame, text="Bild Vektorisierer", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Ordner Auswahl
        ttk.Label(main_frame, text="Bilder Ordner:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        folder_frame = ttk.Frame(main_frame)
        folder_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.selected_folder, 
                                     width=50, state="readonly")
        self.folder_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(folder_frame, text="Durchsuchen", 
                  command=self.select_folder).grid(row=0, column=1)
        
        folder_frame.columnconfigure(0, weight=1)
        
        # Threshold Einstellung
        ttk.Label(main_frame, text="Threshold Wert (0-255):").grid(row=3, column=0, sticky=tk.W, pady=5)
        
        threshold_frame = ttk.Frame(main_frame)
        threshold_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.threshold_scale = ttk.Scale(threshold_frame, from_=0, to=255, 
                                        variable=self.threshold_value, orient=tk.HORIZONTAL)
        self.threshold_scale.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.threshold_label = ttk.Label(threshold_frame, text="128")
        self.threshold_label.grid(row=0, column=1)
        
        self.threshold_value.trace('w', self.update_threshold_label)
        
        threshold_frame.columnconfigure(0, weight=1)
        
        # Unterstützte Formate Info
        info_label = ttk.Label(main_frame, 
                              text="Unterstützte Formate: PNG, JPG, JPEG, BMP, TIFF",
                              font=("Arial", 9), foreground="gray")
        info_label.grid(row=5, column=0, columnspan=2, pady=(0, 15))
        
        # Progress Bar
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                           maximum=100)
        self.progress_bar.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status Label
        self.status_label = ttk.Label(main_frame, text="Bereit zum Vektorisieren")
        self.status_label.grid(row=7, column=0, columnspan=2, pady=(0, 15))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=10)
        
        self.start_button = ttk.Button(button_frame, text="Vektorisierung starten", 
                                      command=self.start_vectorization)
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(button_frame, text="Beenden", 
                  command=self.root.quit).grid(row=0, column=1)
        
        # Grid Konfiguration
        main_frame.columnconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
    def update_threshold_label(self, *args):
        self.threshold_label.config(text=str(int(self.threshold_value.get())))
        
    def select_folder(self):
        folder = filedialog.askdirectory(title="Wählen Sie den Bilder-Ordner")
        if folder:
            self.selected_folder.set(folder)
            
    def get_image_files(self, folder_path):
        """Findet alle unterstützten Bilddateien im Ordner"""
        supported_formats = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif'}
        image_files = []
        
        for file_path in Path(folder_path).iterdir():
            if file_path.is_file() and file_path.suffix.lower() in supported_formats:
                image_files.append(file_path)
                
        return image_files
        
    def convert_to_bitmap(self, image_path, threshold):
        """Konvertiert ein Bild zu einem Schwarz-Weiß Bitmap"""
        try:
            # Bild laden und zu Graustufen konvertieren
            img = Image.open(image_path).convert('L')
            
            # Threshold anwenden
            img = img.point(lambda x: 255 if x > threshold else 0, mode='1')
            
            return img
        except Exception as e:
            raise Exception(f"Fehler beim Konvertieren von {image_path}: {str(e)}")
            
    def bitmap_to_svg(self, bitmap_img, output_path):
        """Konvertiert ein Bitmap zu SVG mit potrace"""
        try:
            # Temporäre PBM Datei erstellen
            with tempfile.NamedTemporaryFile(suffix='.pbm', delete=False) as temp_file:
                temp_pbm = temp_file.name
                
            # Bitmap als PBM speichern
            bitmap_img.save(temp_pbm)
            
            # potrace ausführen
            cmd = [
                self.get_potrace_path(),
                '-s',  # SVG output
                '-o', str(output_path),
                temp_pbm
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Temporäre Datei löschen
            os.unlink(temp_pbm)
            
            if result.returncode != 0:
                raise Exception(f"Potrace Fehler: {result.stderr}")
                
        except Exception as e:
            raise Exception(f"Fehler bei SVG Konvertierung: {str(e)}")
            
    def get_potrace_path(self):
        """Gibt den Pfad zu potrace zurück - plattformspezifisch"""
        if getattr(sys, 'frozen', False):
            # Wenn als exe ausgeführt
            base_path = sys._MEIPASS
        else:
            # Wenn als Python Script ausgeführt
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        system = platform.system().lower()
        
        if system == 'windows':
            potrace_path = os.path.join(base_path, 'potrace', 'potrace.exe')
        elif system == 'darwin':  # macOS
            # Erst im lokalen Ordner schauen, dann im System
            potrace_path = os.path.join(base_path, 'potrace', 'potrace')
            if not os.path.exists(potrace_path):
                # Versuche Homebrew potrace
                potrace_path = '/opt/homebrew/bin/potrace'
                if not os.path.exists(potrace_path):
                    # Versuche MacPorts oder andere Installationen
                    potrace_path = '/usr/local/bin/potrace'
        else:  # Linux und andere Unix-Systeme
            potrace_path = os.path.join(base_path, 'potrace', 'potrace')
            if not os.path.exists(potrace_path):
                # Versuche System-Installation
                potrace_path = '/usr/bin/potrace'
                if not os.path.exists(potrace_path):
                    potrace_path = '/usr/local/bin/potrace'
        
        if not os.path.exists(potrace_path):
            error_msg = f"Potrace nicht gefunden für {system}.\n\n"
            if system == 'darwin':
                error_msg += "Installieren Sie potrace mit: brew install potrace"
            elif system == 'windows':
                error_msg += "Stellen Sie sicher, dass potrace.exe im potrace/ Ordner vorhanden ist."
            else:
                error_msg += "Installieren Sie potrace mit: sudo apt-get install potrace (Ubuntu/Debian)\noder: sudo yum install potrace (CentOS/RHEL)"
            raise Exception(error_msg)
            
        return potrace_path
        
    def start_vectorization(self):
        if not self.selected_folder.get():
            messagebox.showerror("Fehler", "Bitte wählen Sie einen Ordner aus.")
            return
            
        folder_path = Path(self.selected_folder.get())
        if not folder_path.exists():
            messagebox.showerror("Fehler", "Der ausgewählte Ordner existiert nicht.")
            return
            
        # Bilddateien finden
        image_files = self.get_image_files(folder_path)
        if not image_files:
            messagebox.showwarning("Warnung", "Keine unterstützten Bilddateien im Ordner gefunden.")
            return
            
        # Output Ordner erstellen
        output_folder = folder_path / "output"
        output_folder.mkdir(exist_ok=True)
        
        # UI für Verarbeitung vorbereiten
        self.start_button.config(state="disabled")
        self.progress_var.set(0)
        
        try:
            threshold = int(self.threshold_value.get())
            total_files = len(image_files)
            
            for i, image_file in enumerate(image_files):
                # Status aktualisieren
                self.status_label.config(text=f"Verarbeite: {image_file.name}")
                self.root.update()
                
                try:
                    # Zu Bitmap konvertieren
                    bitmap_img = self.convert_to_bitmap(image_file, threshold)
                    
                    # SVG Ausgabepfad
                    svg_output = output_folder / f"{image_file.stem}.svg"
                    
                    # Zu SVG konvertieren
                    self.bitmap_to_svg(bitmap_img, svg_output)
                    
                except Exception as e:
                    print(f"Fehler bei {image_file.name}: {str(e)}")
                    continue
                    
                # Progress aktualisieren
                progress = ((i + 1) / total_files) * 100
                self.progress_var.set(progress)
                self.root.update()
                
            # Fertig
            self.status_label.config(text=f"Fertig! {total_files} Bilder verarbeitet.")
            messagebox.showinfo("Erfolg", 
                              f"Vektorisierung abgeschlossen!\n"
                              f"{total_files} Bilder wurden verarbeitet.\n"
                              f"Ausgabe in: {output_folder}")
                              
        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {str(e)}")
            self.status_label.config(text="Fehler bei der Verarbeitung")
            
        finally:
            self.start_button.config(state="normal")
            self.progress_var.set(0)

def main():
    root = tk.Tk()
    app = VectorizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 