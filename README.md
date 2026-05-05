# 🚀 AutoOps AI Frontend

Modern React-based dashboard for AutoOps AI backend. Provides beautiful UI for analyzing SaaS user inactivity and optimizing costs.

## Features

✨ **Real-time Dashboard** - Live analytics and insights  
📊 **Analysis Tools** - Run analysis and generate reports  
📧 **Email Integration** - Send reports directly to email  
📄 **PDF Export** - Download professional reports  
📈 **Report History** - Track all analysis over time  
⚙️ **Settings** - Customize thresholds and preferences  
🎨 **Modern UI** - Built with React + Tailwind CSS  
📱 **Responsive** - Works on desktop and mobile  

## Tech Stack

- **Framework:** React 18.2
- **Styling:** Tailwind CSS
- **Build:** Vite
- **HTTP Client:** Axios
- **Icons:** Lucide React
- **Bundler:** Vite

## Installation

### Prerequisites
- Node.js 16+ 
- npm or yarn
- AutoOps backend running on `localhost:8000`

### Setup

1. **Install dependencies**
```bash
npm install
```

2. **Start development server**
```bash
npm run dev
```

Frontend will open at `http://localhost:3000`

3. **Build for production**
```bash
npm run build
```

## File Structure

```
src/
├── components/
│   ├── Dashboard.jsx      # Main analytics dashboard
│   ├── Analysis.jsx       # Analysis & email tools
│   ├── Reports.jsx        # Report history
│   └── Settings.jsx       # Configuration
├── App.jsx                # Main app component
├── api.js                 # Backend API integration
├── main.jsx               # React entry point
└── index.css              # Tailwind styles
```

## Components

### Dashboard
- Real-time analytics
- Inactive users count
- Monthly savings calculation
- AI insights
- User detail table

### Analysis
- Run analysis with email
- Send formatted reports
- Export to PDF
- How-it-works guide

### Reports
- View all historical reports
- Report statistics
- Clear reports
- User details per report

### Settings
- System health status
- Application settings
- API configuration
- Service status

## API Integration

All backend endpoints are integrated:

| Endpoint | Purpose |
|----------|---------|
| `GET /` | Welcome message |
| `GET /analyze` | Run analysis |
| `GET /analyze-email/{email}` | Analyze & email |
| `POST /send-email` | Send report email |
| `GET /export` | Download PDF |
| `GET /reports` | Get report history |
| `GET /health` | System health |
| `GET /stats` | Statistics |

## Environment Configuration

Backend API is configured to `http://localhost:8000`

To change, edit `src/api.js`:
```javascript
const API_BASE = 'http://your-backend-url:8000';
```

## Styling

Built with Tailwind CSS. Custom utilities in `src/index.css`:

```css
.btn-primary     /* Primary button */
.btn-secondary   /* Secondary button */
.btn-danger      /* Danger button */
.card            /* Card container */
.input-field     /* Input styling */
.stat-card       /* Statistics card */
.badge           /* Badge tag */
```

## Features Guide

### 📊 Dashboard
- View key metrics at a glance
- See inactive users and savings
- Quick action buttons
- Real-time updates

### 🔍 Analysis
- **Run Analysis:** View current user status
- **Send Email:** Send report to team
- **Export PDF:** Download professional report

### 📁 Reports
- View all past analyses
- Track savings over time
- Clear old reports
- Detailed user information

### ⚙️ Settings
- Configure cost per user
- Adjust inactivity threshold
- Email notifications toggle
- View system health

## Customization

### Change Colors
Edit `tailwind.config.js` theme colors

### Add New Pages
1. Create component in `src/components/`
2. Add to navigation in `App.jsx`
3. Import and render

### Modify API Calls
Edit `src/api.js` to add/change endpoints

## Deployment

### Build
```bash
npm run build
```

Output in `dist/` folder

### Deploy Options
- Vercel (recommended)
- Netlify
- GitHub Pages
- AWS S3 + CloudFront
- Firebase Hosting

### Vercel Deploy
```bash
npm install -g vercel
vercel
```

## Performance

- ⚡ Fast with Vite
- 🎨 Optimized CSS
- 📦 Lazy loading components
- 🔄 Efficient API calls

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Troubleshooting

### Backend not connecting
- Ensure backend is running on `localhost:8000`
- Check CORS is enabled in backend
- Verify API endpoints in `/docs`

### Build errors
```bash
npm clean-install
npm run build
```

### Port 3000 in use
Change in `vite.config.js`:
```javascript
server: {
    port: 3001,  // Change port
}
```

## Development

### Run with auto-reload
```bash
npm run dev
```

### Debug API calls
Open browser DevTools → Network tab

### Inspect components
Install React DevTools browser extension

## Contributing

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## License

MIT License - See LICENSE file

## Support

- Docs: http://localhost:8000/docs
- GitHub: [AutoOps AI](https://github.com)
- Email: support@autoops.ai

## Roadmap

- [ ] Dark/Light theme toggle
- [ ] Export to CSV
- [ ] Scheduled reports
- [ ] Slack integration
- [ ] User management
- [ ] Advanced analytics
- [ ] Multi-company support
- [ ] API key management

---

**Version:** 1.0.0  
**Status:** Production Ready  
**Last Updated:** May 2026
