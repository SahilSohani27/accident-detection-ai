# 🚨 AI Accident Alert Dashboard

A modern, attractive Streamlit-based web interface for the AI Accident Alert System. This dashboard provides an intuitive way to upload videos, monitor processing status, and view accident detection results.

## ✨ Features

- **🎨 Modern UI Design**: Beautiful gradient-based interface with smooth animations
- **📤 Video Upload**: Drag-and-drop video upload with file validation
- **📹 Sample Videos**: Pre-loaded sample videos for testing the system
- **🔄 Real-time Processing**: Live status updates during video analysis
- **📊 Results Display**: Comprehensive accident detection results and statistics
- **📱 QR Code Integration**: Easy access to emergency Telegram channel
- **🚨 SOS Generation**: AI-powered emergency message generation
- **📱 Telegram Alerts**: Automatic emergency notifications

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Backend API running on `http://localhost:8000`

### Installation

1. **Navigate to the dashboard directory:**
   ```bash
   cd dashboard
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard:**
   ```bash
   python run_dashboard.py
   ```
   
   Or manually:
   ```bash
   streamlit run dashboard.py
   ```

4. **Open your browser:**
   Navigate to `http://localhost:8501`

## 🎯 Usage

### Uploading Videos

1. **Select a video file** using the file uploader
2. **Click "Analyze Video"** to start processing
3. **Monitor progress** through the step indicator
4. **View results** when processing is complete

### Sample Videos

- Click on any sample video in the sidebar to test the system
- Sample videos are pre-loaded for demonstration purposes
- Perfect for hackathon demonstrations and testing

### Emergency Channel

- **QR Code**: Scan the QR code in the sidebar to join the emergency channel
- **Direct Link**: Click the "Join Telegram Channel" button
- **Real-time Alerts**: Receive instant notifications when accidents are detected

## 🎨 UI Components

### Main Interface
- **Header**: Project branding with gradient background
- **Upload Area**: Drag-and-drop video upload interface
- **Progress Indicator**: 6-step processing visualization
- **Results Panel**: Comprehensive analysis results display

### Sidebar
- **Sample Videos**: Quick access to test videos
- **QR Code**: Emergency channel access
- **System Status**: Real-time system health indicators
- **Technical Specs**: System capabilities and limitations

### Status Cards
- **Success Cards**: Green gradient for successful operations
- **Error Cards**: Red gradient for error messages
- **Status Cards**: Blue gradient for processing information

## 🔧 Configuration

### Backend API
Update the backend URL in `dashboard.py`:
```python
BACKEND_URL = "http://localhost:8000"  # Change if different
```

### Telegram Channel
Update the channel link:
```python
TELEGRAM_CHANNEL_LINK = "https://t.me/your_accident_alert_channel"
```

## 📱 Mobile Responsive

The dashboard is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- Various screen sizes

## 🎨 Customization

### Colors and Themes
The dashboard uses CSS custom properties for easy theming:
- Primary gradient: `#667eea` to `#764ba2`
- Success gradient: `#4facfe` to `#00f2fe`
- Error gradient: `#ff416c` to `#ff4b2b`

### Adding New Features
1. Add new components in the main function
2. Update the sidebar for new navigation items
3. Modify the CSS for styling changes

## 🐛 Troubleshooting

### Common Issues

1. **Backend Connection Error**
   - Ensure the backend API is running
   - Check the BACKEND_URL configuration
   - Verify the API endpoint is accessible

2. **Video Upload Issues**
   - Check file format (MP4, AVI, MOV, MKV)
   - Ensure file size is under 50MB
   - Verify file is not corrupted

3. **QR Code Not Displaying**
   - Check if qrcode[pil] is installed
   - Verify Pillow installation

## 📊 Performance

- **Upload Speed**: Depends on file size and network
- **Processing Time**: 10-30 seconds for typical videos
- **Memory Usage**: Optimized for efficient processing
- **Concurrent Users**: Supports multiple simultaneous uploads

## 🔒 Security

- File type validation
- Size limit enforcement
- Secure API communication
- Input sanitization

## 📈 Future Enhancements

- Real-time video streaming
- Batch processing capabilities
- Advanced analytics dashboard
- User authentication system
- Cloud storage integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the AI Accident Alert System and follows the same licensing terms.

---

**Built with ❤️ for emergency response and public safety**
