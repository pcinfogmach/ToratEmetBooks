import os
from collections import defaultdict

# נתיב לריפוזיטורי
repo_path = '.'

# שם קובץ הפלט
output_file = 'index.html'

# קוד HTML ראשוני עם Bootstrap 5 RTL ושיפורי עיצוב
header = '''<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>רשימת דפי HTML - ספרי תורת אמת</title>
    <!-- Google Fonts - Alef ו-Open Sans -->
    <link href="https://fonts.googleapis.com/css2?family=Alef&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
    <!-- Bootstrap 5 RTL CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css" rel="stylesheet" integrity="sha384-ENjdO4Dr2bkBIFxQpeo5Kw92C5rN6QbXmk6bRrZfP9a4rKsbM5moq0j3vP5o7en" crossorigin="anonymous">
    <!-- Bootstrap Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
    <!-- קובץ CSS מותאם אישית -->
    <style>
        body {
            font-family: 'Alef', 'Open Sans', sans-serif;
            background-color: #f8f9fa;
            padding-top: 70px; /* רווח לתפריט הניווט הקבוע */
            transition: background-color 0.3s ease;
        }
        h1 {
            margin-bottom: 40px;
            text-align: center;
            color: #2c3e50;
            font-weight: 600;
            font-size: 2.5rem;
        }
        .folder-name {
            margin-top: 50px;
            margin-bottom: 20px;
            color: #34495e;
            font-size: 2rem;
            border-bottom: 3px solid #bdc3c7;
            padding-bottom: 10px;
            display: flex;
            align-items: center;
        }
        .folder-name .bi-folder-fill {
            margin-left: 10px;
            font-size: 1.8rem;
            color: #3498db;
        }
        .book-card {
            margin-bottom: 20px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .book-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        }
        .book-title {
            font-size: 1.1rem;
            font-weight: 500;
            color: #2980b9;
            text-align: center;
            margin-top: 10px;
            text-decoration: none;
            transition: color 0.3s ease;
        }
        .book-title:hover {
            color: #1abc9c;
            text-decoration: underline;
        }
        .search-bar {
            margin-bottom: 30px;
        }
        /* עיצוב חלונית החיפוש */
        .search-bar input {
            height: 60px;
            font-size: 1.2rem;
            border-radius: 30px;
            padding: 0 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border: 2px solid #3498db;
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
        }
        .search-bar input:focus {
            border-color: #1abc9c;
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            outline: none;
        }
        /* נגיעות נוספות לשיפור הנראות */
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        footer {
            text-align: center;
            margin-top: 50px;
            color: #7f8c8d;
            font-size: 1rem;
        }
    </style>
</head>
<body>

    <div class="container">
        <h1>רשימת דפי HTML - ספרי תורת אמת</h1>
        <!-- שדה חיפוש -->
        <div class="row justify-content-center search-bar">
            <div class="col-md-8">
                <input type="text" class="form-control" id="searchInput" placeholder="חיפוש ספרים...">
            </div>
        </div>
'''

footer = '''
        <footer>
            &copy; 2024 ספרי תורת אמת. כל הזכויות שמורות.
        </footer>
    </div>
    <!-- Bootstrap JS ו-Popper.js -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+6cHqfC+58iwbX2weFrbE8c+gHkg6" crossorigin="anonymous"></script>
    <!-- JavaScript מותאם אישית לחיפוש -->
    <script>
        document.getElementById('searchInput').addEventListener('keyup', function() {
            const filter = this.value.toLowerCase();
            const categories = document.querySelectorAll('.folder-name');
    
            categories.forEach(function(category) {
                const row = category.nextElementSibling; // השורה שקשורה לקטגוריה
                const cards = row.querySelectorAll('.book-card');
    
                let hasVisibleBooks = false;
    
                cards.forEach(function(card) {
                    const title = card.querySelector('.book-title').textContent.toLowerCase();
                    if (title.includes(filter)) {
                        card.style.display = '';
                        hasVisibleBooks = true;
                    } else {
                        card.style.display = 'none';
                    }
                });
    
                // אם אין כרטיסים נראים, הסתר את הכותרת והקטגוריה
                if (hasVisibleBooks) {
                    category.style.display = '';
                    row.style.display = '';
                } else {
                    category.style.display = 'none';
                    row.style.display = 'none';
                }
            });
        });
    </script>
</body>
</html>
'''

# מילון לאחסון תיקיות וקבצים
dir_files = defaultdict(list)

for root, dirs, files in os.walk(repo_path):
    for file in files:
        if file.endswith('.html') and file != 'index.html':
            path = os.path.join(root, file)
            relative_path = os.path.relpath(path, repo_path)
            relative_path = relative_path.replace('\\', '/')
            dir_name = os.path.dirname(relative_path)
            dir_files[dir_name].append(relative_path)

# מיון התיקיות
sorted_dirs = sorted(dir_files.keys())

list_items = ''

for dir in sorted_dirs:
    if dir == '.':
        list_items += '<div class="folder-name"><i class="bi bi-folder-fill"></i> קבצים בשורש:</div>\n'
    else:
        folder_display = dir.replace('_', ' ').replace('/', ' / ')
        list_items += f'<div class="folder-name"><i class="bi bi-folder-fill"></i> {folder_display}</div>\n'
    
    list_items += '<div class="row">\n'
    
    for file in sorted(dir_files[dir]):
        display_name = os.path.splitext(os.path.basename(file))[0]
        display_name = display_name.replace('_', ' ')
        list_items += f'''    <div class="col-lg-3 col-md-4 col-sm-6">
            <div class="card book-card">
                <div class="card-body text-center">
                    <a href="{file}" class="book-title">{display_name}</a>
                </div>
            </div>
        </div>\n'''
    
    list_items += '</div>\n'

# שילוב כל החלקים
full_html = header + list_items + footer

# כתיבה ל-`index.html`
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f'נוצר {output_file} עם {len(dir_files)} תיקיות.')
