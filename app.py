#!/usr/bin/env python3
"""
Film Cinemax Desktop Application
A professional GUI application for managing film collections
"""

import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QTableWidget, QTableWidgetItem,
    QDialog, QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont


class FilmDialog(QDialog):
    """Dialog for adding/editing films"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Film")
        self.setGeometry(100, 100, 450, 300)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Name field
        layout.addWidget(QLabel("Film Name:"))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)
        
        # Director field
        layout.addWidget(QLabel("Director:"))
        self.director_input = QLineEdit()
        layout.addWidget(self.director_input)
        
        # Year field
        layout.addWidget(QLabel("Year:"))
        self.year_input = QLineEdit()
        layout.addWidget(self.year_input)
        
        # Category field
        layout.addWidget(QLabel("Category:"))
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Drama", "Crime", "Action", "Sci-Fi", "Romance", "Animation"])
        layout.addWidget(self.category_combo)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_data(self):
        """Return film data as dictionary"""
        try:
            return {
                'name': self.name_input.text().strip(),
                'director': self.director_input.text().strip(),
                'year': int(self.year_input.text().strip()),
                'category': self.category_combo.currentText()
            }
        except ValueError:
            return None


class FilmCinemaxApp(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Film Box")
        self.setGeometry(100, 100, 1000, 700)
        self.base_url = "http://localhost:5000/api"
        self.selected_film_id = None
        self.retry_count = 0
        self.init_ui()
        
        # Auto-load films on startup with retry
        QTimer.singleShot(1000, self.load_all_films_with_retry)
    
    def init_ui(self):
        """Initialize the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        
        # Title
        title = QLabel("Film Box")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)
        
        # Control panel
        control_layout = QHBoxLayout()
        
        # Category filter
        control_layout.addWidget(QLabel("Category:"))
        self.category_combo = QComboBox()
        self.category_combo.addItems(["All", "Drama", "Crime", "Action", "Sci-Fi", "Romance", "Animation"])
        control_layout.addWidget(self.category_combo)
        
        load_btn = QPushButton("Load")
        load_btn.clicked.connect(self.load_by_category)
        control_layout.addWidget(load_btn)
        
        # Search
        control_layout.addWidget(QLabel("Film Name:"))
        self.search_input = QLineEdit()
        self.search_input.setMaximumWidth(300)
        self.search_input.returnPressed.connect(self.search_films)
        control_layout.addWidget(self.search_input)
        
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search_films)
        control_layout.addWidget(search_btn)
        
        # Action buttons
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self.delete_film)
        control_layout.addWidget(delete_btn)
        
        add_btn = QPushButton("Add Film")
        add_btn.clicked.connect(self.open_film_dialog)
        control_layout.addWidget(add_btn)
        
        sort_btn = QPushButton("Sort by Year")
        sort_btn.clicked.connect(self.sort_by_year)
        control_layout.addWidget(sort_btn)
        
        main_layout.addLayout(control_layout)
        
        # Films table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Film Name", "Director", "Year", "Category"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.itemSelectionChanged.connect(self.on_film_select)
        main_layout.addWidget(self.table)
        
        # Status bar
        self.status_label = QLabel("Ready")
        main_layout.addWidget(self.status_label)
        
        central_widget.setLayout(main_layout)
    
    def make_request(self, method, endpoint, **kwargs):
        """Make HTTP request to backend"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.request(method, url, timeout=10, **kwargs)
            if response.status_code == 200 or response.status_code == 201:
                data = response.json()
                # Extract the 'data' field if the response has it
                if isinstance(data, dict) and 'data' in data:
                    return data['data']
                return data
            else:
                self.status_label.setText(f"Server error: {response.status_code}")
                return None
        except requests.exceptions.Timeout:
            self.status_label.setText("Connection timeout - Flask might still be starting")
            return None
        except requests.exceptions.ConnectionError:
            self.status_label.setText("Cannot connect to Flask on localhost:5000")
            return None
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
            return None
    
    def load_all_films(self):
        """Load all films from backend"""
        response = self.make_request('GET', '/media')
        if response:
            self.display_films(response)
            self.status_label.setText(f"Loaded {len(response)} films")
        else:
            self.status_label.setText("Failed to load films")
    
    def load_all_films_with_retry(self):
        """Load films with automatic retry"""
        response = self.make_request('GET', '/media')
        if response:
            self.display_films(response)
            self.status_label.setText(f"✓ Loaded {len(response)} films")
            self.retry_count = 0
        else:
            self.retry_count += 1
            if self.retry_count < 5:
                self.status_label.setText(f"Retrying... (attempt {self.retry_count}/5)")
                QTimer.singleShot(2000, self.load_all_films_with_retry)
            else:
                self.status_label.setText("Failed to connect to Flask backend")
    
    def load_by_category(self):
        """Load films by category"""
        category = self.category_combo.currentText()
        if category == "All":
            self.load_all_films()
        else:
            response = self.make_request('GET', f'/media/category/{category}')
            if response:
                self.display_films(response)
                self.status_label.setText(f"Loaded {len(response)} films in {category}")
            else:
                self.status_label.setText(f"Failed to load {category}")
    
    def search_films(self):
        """Search films"""
        query = self.search_input.text().strip()
        if not query:
            QMessageBox.warning(self, "Input Required", "Please enter a film name or director")
            return
        
        response = self.make_request('GET', f'/films?search={query}')
        if response:
            self.display_films(response)
            self.status_label.setText(f"Found {len(response)} match(es)")
        else:
            self.status_label.setText("No results found")
    
    def display_films(self, films):
        """Display films in table"""
        self.table.setRowCount(0)
        for i, film in enumerate(films):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(film['name']))
            # Use 'author' if 'director' doesn't exist (backend uses 'author')
            director = film.get('director') or film.get('author', 'N/A')
            self.table.setItem(i, 1, QTableWidgetItem(director))
            # Use 'publication_date' if 'year' doesn't exist
            year = film.get('year') or film.get('publication_date', 'N/A')
            self.table.setItem(i, 2, QTableWidgetItem(str(year)))
            self.table.setItem(i, 3, QTableWidgetItem(film.get('category', 'Film')))
            # Store film ID in first column item
            self.table.item(i, 0).film_id = str(film['id'])
    
    def on_film_select(self):
        """Handle film selection"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.selected_film_id = self.table.item(current_row, 0).film_id
    
    def open_film_dialog(self):
        """Open add film dialog"""
        dialog = FilmDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if not data:
                QMessageBox.warning(self, "Invalid Input", "Please enter a valid year")
                return
            
            if not all(data.values()):
                QMessageBox.warning(self, "Incomplete", "Please fill all fields")
                return
            
            response = self.make_request('POST', '/films', json=data)
            if response:
                QMessageBox.information(self, "Success", "Film added successfully")
                self.load_all_films()
            else:
                QMessageBox.critical(self, "Error", "Failed to add film")
    
    def delete_film(self):
        """Delete selected film"""
        if not self.selected_film_id:
            QMessageBox.warning(self, "No Selection", "Please select a film to delete")
            return
        
        current_row = self.table.currentRow()
        film_name = self.table.item(current_row, 0).text()
        
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete '{film_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            response = self.make_request('DELETE', f'/films/{self.selected_film_id}')
            if response:
                QMessageBox.information(self, "Success", "Film deleted successfully")
                self.load_all_films()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete film")
    
    def sort_by_year(self):
        """Sort films by year"""
        self.table.sortItems(2, Qt.SortOrder.DescendingOrder)
        self.status_label.setText("Sorted by year (newest first)")


def main():
    """Run the application"""
    app = QApplication(sys.argv)
    window = FilmCinemaxApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
