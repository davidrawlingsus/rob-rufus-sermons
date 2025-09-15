# 🎵 Rob Rufus Sermon Directory

A mobile-first, interactive directory for browsing and accessing 559 Rob Rufus sermons from 2004-2024, featuring optimized thematic filtering, real-time search, and responsive design.

![Sermon Directory Preview](https://img.shields.io/badge/Sermons-559-blue) ![Date Range](https://img.shields.io/badge/Years-2004--2024-green) ![Themes](https://img.shields.io/badge/Themes-21-orange)

## ✨ Features

### 🔍 **Smart Search & Filtering**
- **Real-time search** by title, theme, or date
- **Optimized thematic filter chips** based on content analysis
- **Mobile-first design** with expandable theme options
- **Multi-filter support** with live statistics

### 📱 **Responsive Design**
- **Mobile-optimized** interface with touch-friendly controls
- **Sticky filters** for easy access while scrolling
- **Progressive enhancement** for desktop users
- **Accessible** with proper keyboard navigation

### 🎯 **Intelligent Thematic Organization**
Sermons are automatically categorized using advanced keyword analysis:

**Core Themes (Mobile-First):**
- Grace & Gospel (113 sermons)
- Anointing & Power (184 sermons)
- Holy Spirit (140 sermons)
- Faith & Trust (69 sermons)
- Worship & Praise (149 sermons)
- Healing & Miracles (103 sermons)
- Kingdom & Authority (80 sermons)
- Freedom & Liberation (99 sermons)

**Extended Themes (Desktop):**
- Spiritual Warfare, Fear & Courage, Word & Truth, Peace & Rest
- Prayer & Intercession, Identity & Sonship, Joy & Happiness
- Church & Ministry, Christmas & Easter, End Times & Prophecy
- Discipleship & Growth, Testimonies & Reports

### 📅 **Flexible Sorting & Organization**
- **Newest First** (default)
- **Oldest First**
- **Title A-Z**
- **Title Z-A**

## 🚀 Quick Start

### Option 1: Use the Directory (Recommended)
1. **Download** the repository
2. **Run** the scraper to download sermons:
   ```bash
   python3 rob_rufus_scraper.py
   ```
3. **Open** `sermon_directory.html` in your browser
4. **Start browsing** and filtering sermons!

### Option 2: Development Setup
1. **Clone** the repository:
   ```bash
   git clone https://github.com/yourusername/rob-rufus-sermons.git
   cd rob-rufus-sermons
   ```

2. **Install** dependencies:
   ```bash
   python3 setup.py
   # or manually:
   pip install -r requirements.txt
   ```

3. **Run** the scraper:
   ```bash
   python3 rob_rufus_scraper.py
   ```

4. **Open** the directory:
   ```bash
   python3 demo.py
   ```

## 📁 Project Structure

```
rob-rufus-sermons/
├── 📄 sermon_directory.html      # Main interactive directory
├── 🐍 rob_rufus_scraper.py       # Sermon downloader
├── 🐍 analyze_sermons.py         # Metadata extraction
├── 🐍 update_themes.py           # Theme optimization
├── 🐍 demo.py                    # Demo script
├── 📊 sermon_metadata.json       # Sermon data (generated)
├── 📁 Rob_Rufus_Sermons/         # MP3 files (downloaded)
├── 📋 requirements.txt           # Python dependencies
├── ⚙️  setup.py                   # Setup script
└── 📖 README.md                  # This file
```

## 🛠️ Technical Details

### **Architecture**
- **Pure HTML/CSS/JavaScript** - no external dependencies
- **Python backend** for data processing and scraping
- **Mobile-first responsive design** with CSS Grid and Flexbox
- **Client-side filtering** for fast performance

### **Data Processing**
- **Intelligent theme extraction** using keyword analysis
- **Automatic date parsing** from filenames
- **Optimized categorization** based on content analysis
- **JSON metadata** for fast loading

### **Performance**
- **Fast client-side filtering** with minimal DOM manipulation
- **Efficient search** with real-time results
- **Smooth animations** with CSS transitions
- **Responsive images** and touch interactions

## 🎨 Customization

### **Adding New Themes**
Edit `update_themes.py` to modify theme keywords:
```python
theme_keywords = {
    'Your Theme': ['keyword1', 'keyword2', 'keyword3'],
    # ... existing themes
}
```

### **Styling**
Modify CSS variables in `sermon_directory.html`:
```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --text-color: #333;
    /* ... other variables */
}
```

### **Filter Chips**
Update the mobile-first theme list in the JavaScript:
```javascript
const mobileThemes = [
    'Your Theme',
    'Another Theme',
    // ... existing themes
];
```

## 📊 Statistics

- **559 total sermons** spanning 20 years
- **21 thematic categories** with intelligent classification
- **2004-2024 date range** covering Rob Rufus's ministry
- **Mobile-optimized** with 8 primary filter chips
- **Desktop-enhanced** with 12+ additional themes

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### **Development Guidelines**
- Follow mobile-first design principles
- Maintain accessibility standards
- Test on multiple devices and browsers
- Update documentation for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Rob Rufus** for his powerful teaching ministry
- **City Church International** for hosting the sermons
- **Open source community** for the tools and libraries used

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/rob-rufus-sermons/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/rob-rufus-sermons/discussions)
- **Email**: your.email@example.com

---

*Built with ❤️ for the Rob Rufus teaching ministry community*