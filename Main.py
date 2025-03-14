import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from venv import EnvBuilder

class VirtualEnvCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Creador de Entornos Virtuales")
        
        # Configurar la interfaz
        self.create_widgets()
        
    def create_widgets(self):
        # Marco principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Entrada para directorio
        ttk.Label(main_frame, text="Directorio de guardado:").grid(row=0, column=0, sticky=tk.W)
        self.directory = tk.StringVar()
        dir_entry = ttk.Entry(main_frame, textvariable=self.directory, width=40)
        dir_entry.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Botón para buscar directorio
        ttk.Button(main_frame, text="Examinar...", command=self.browse_directory).grid(
            row=1, column=1, sticky=tk.W, padx=5)
            
        # Entrada para nombre del entorno
        ttk.Label(main_frame, text="Nombre del entorno:").grid(row=2, column=0, sticky=tk.W, pady=(10,0))
        self.env_name = tk.StringVar()
        name_entry = ttk.Entry(main_frame, textvariable=self.env_name, width=40)
        name_entry.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        # Botón de creación
        ttk.Button(main_frame, text="Crear Entorno", command=self.create_virtualenv).grid(
            row=4, column=0, columnspan=2, pady=20)
            
        # Área de estado
        self.status = tk.Text(main_frame, height=4, width=50, state=tk.DISABLED)
        self.status.grid(row=5, column=0, columnspan=2)
        
        # Configurar el redimensionamiento
        main_frame.columnconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory.set(directory)
            
    def update_status(self, message):
        self.status.config(state=tk.NORMAL)
        self.status.delete(1.0, tk.END)
        self.status.insert(tk.END, message)
        self.status.config(state=tk.DISABLED)
        
    def create_virtualenv(self):
        directory = self.directory.get()
        env_name = self.env_name.get()
        
        if not directory or not env_name:
            messagebox.showerror("Error", "Por favor completa todos los campos")
            return
            
        env_path = os.path.join(directory, env_name)
        
        if os.path.exists(env_path):
            respuesta = messagebox.askyesno(
                "Directorio existente",
                f"El directorio {env_path} ya existe. ¿Deseas eliminarlo y continuar?"
            )
            if respuesta:
                try:
                    shutil.rmtree(env_path)
                except Exception as e:
                    self.update_status(f"Error al eliminar: {str(e)}")
                    return
            else:
                self.update_status("Creación cancelada")
                return
                
        try:
            self.update_status("Creando entorno virtual...")
            self.root.update_idletasks()  # Actualizar la interfaz
            
            # Crear el entorno virtual
            builder = EnvBuilder(with_pip=True)
            builder.create(env_path)
            
            self.update_status(f"Entorno creado exitosamente en:\n{env_path}")
            messagebox.showinfo("Éxito", "Entorno virtual creado correctamente")
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            messagebox.showerror("Error", f"No se pudo crear el entorno:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualEnvCreator(root)
    root.mainloop()