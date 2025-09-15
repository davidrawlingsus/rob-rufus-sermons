# Rob Rufus Sermon Directory

A mobile-first, interactive directory for browsing and accessing 559 Rob Rufus sermons from 2004-2024.

## Features

### 🔍 **Search & Filter**
- **Real-time search** by title, theme, or date
- **Thematic filter chips** for quick topic-based browsing
- **Smart filtering** with multiple active filters

### 📱 **Mobile-First Design**
- **Responsive layout** that works on all devices
- **Touch-friendly** interface with large tap targets
- **Sticky filters** for easy access while scrolling

### 🎯 **Thematic Organization**
Sermons are automatically categorized by themes including:
- Grace & Gospel
- Faith & Trust
- Anointing & Power
- Holy Spirit & Manifestation
- Healing & Miracles
- Worship & Praise
- Identity & Sonship
- And many more...

### 📅 **Flexible Sorting**
- **Newest First** (default)
- **Oldest First**
- **Title A-Z**
- **Title Z-A**

### 🎵 **Easy Access**
- **Direct download** links for each sermon
- **Play buttons** (ready for audio player integration)
- **Clean, readable** sermon cards with metadata

## Usage

1. **Open** `sermon_directory.html` in your web browser
2. **Search** using the search bar at the top
3. **Filter** by clicking theme chips (e.g., "Grace", "Faith", "Anointing")
4. **Sort** using the dropdown menu
5. **Download** or play sermons using the action buttons

## File Structure

```
Rob Rufus Sermons/
├── sermon_directory.html      # Main directory interface
├── sermon_metadata.json       # Sermon data and metadata
├── analyze_sermons.py         # Script to analyze sermon files
├── Rob_Rufus_Sermons/         # Directory containing MP3 files
│   ├── 2024-10-27_An_Anointing_That_Goes_Beyond_Just_Yourself.mp3
│   ├── 2024-10-20_Encounters_with_God_Rob_Rufus.mp3
│   └── ... (559 total sermons)
└── DIRECTORY_README.md        # This file
```

## Technical Details

- **Pure HTML/CSS/JavaScript** - no external dependencies
- **Mobile-first responsive design**
- **Accessible** with proper ARIA labels and keyboard navigation
- **Fast filtering** with client-side JavaScript
- **Clean, modern UI** with smooth animations

## Customization

The directory can be easily customized by modifying:

- **CSS variables** for colors and spacing
- **Theme keywords** in `analyze_sermons.py` for different categorization
- **Sorting options** in the JavaScript
- **Visual styling** in the CSS

## Browser Compatibility

Works in all modern browsers including:
- Chrome/Edge (recommended)
- Firefox
- Safari
- Mobile browsers

## Performance

- **Fast loading** with optimized CSS and JavaScript
- **Efficient filtering** with minimal DOM manipulation
- **Smooth animations** with CSS transitions
- **Responsive images** and touch interactions

---

*Generated from 559 Rob Rufus sermons spanning 20 years of ministry (2004-2024)*
