# MediGenAI - Page Layout Guide

## 🎨 Visual Overview of All Pages

This document describes what each page looks like and its key elements.

---

## 1. 🔐 Login Page

**URL**: `/` (root)

**Layout**:
```
┌─────────────────────────────────────────────────┐
│  LEFT SIDE (Gradient)  │  RIGHT SIDE (White)   │
│                        │                        │
│  MediGenAI Title       │    🏥 Icon             │
│  Description           │    Welcome Back        │
│                        │    Sign in to access   │
│  ✓ AI-Powered         │                        │
│  ✓ Real-time Insights │    Username: [____]    │
│  ✓ Secure & Compliant │    Password: [____]    │
│                        │                        │
│                        │    [Sign In Button]    │
│                        │                        │
│                        │    Demo Credentials    │
└─────────────────────────────────────────────────┘
```

**Features**:
- Purple gradient background on left
- Feature highlights with icons
- Modern form design on right
- Responsive layout

**Colors**:
- Gradient: Purple (#667eea) to Violet (#764ba2)
- Background: White (#ffffff)
- Buttons: Gradient purple

---

## 2. 📊 Dashboard

**URL**: `/dashboard/`

**Layout**:
```
┌──────────────────────────────────────────────────────────┐
│ SIDEBAR │  HEADER: Welcome to the Dashboard!            │
│         │  [User Avatar] Admin                           │
├─────────┼────────────────────────────────────────────────┤
│ 🏥 Logo │  📊 STATS CARDS (4 cards in a row)            │
│         │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐         │
│ Dashboard│  │👥123││📄 67││⚠️ 5 ││🤖 8 │         │
│ Patients │  │Patients││Reports││Pending││AI-Gen│         │
│ Reports  │  └──────┘ └──────┘ └──────┘ └──────┘         │
│ AI Analy.│                                                │
│         │  ┌─────────────────┐ ┌──────────────────┐     │
│ Logout  │  │ Add New Patient │ │ AI Analysis     │     │
│         │  │                 │ │                  │     │
│         │  │ Name: [_____]  │ │ 🥧 Donut Chart   │     │
│         │  │ Age:  [_____]  │ │                  │     │
│         │  │ Gender: ○○     │ │ Normal:  10      │     │
│         │  │ Contact:[_____]│ │ At Risk: 3       │     │
│         │  │ [Add Patient]  │ │ Critical: 2      │     │
│         │  └─────────────────┘ └──────────────────┘     │
│         │                                                │
│         │  RECENT PATIENTS TABLE                        │
│         │  ID    │ Patient │ Date │ Status │ Action    │
│         │  REP-067│John Doe │04-12│🟢Normal│[View]    │
│         │  REP-066│Sarah   │04-11│🟡Risk  │[View]    │
└──────────────────────────────────────────────────────────┘
```

**Key Elements**:
- Left sidebar with navigation (fixed)
- 4 statistics cards at top
- Add patient form (left column)
- AI analysis overview (right column)
- Recent patients table below

**Colors**:
- Sidebar: Blue gradient (#1e3a8a to #1e40af)
- Cards: White with shadows
- Status badges: Green/Orange/Red

---

## 3. 👥 Patients Page

**URL**: `/patients/`

**Layout**:
```
┌──────────────────────────────────────────────────────────┐
│ SIDEBAR │  HEADER: Patients                              │
│         │  View and manage all patient records           │
├─────────┼────────────────────────────────────────────────┤
│         │  [Search: _________________] [Search Button]   │
│         │                                                │
│         │  PATIENT CARDS (Grid Layout)                   │
│         │  ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│         │  │👤 S     │ │👤 J     │ │👤 R     │          │
│         │  │Sarah    │ │John Doe │ │Robert   │          │
│         │  │Smith    │ │         │ │Brown    │          │
│         │  │Age: 34  │ │Age: 45  │ │Age: 52  │          │
│         │  │Gender:F │ │Gender:M │ │Gender:M │          │
│         │  │Contact: │ │Contact: │ │Contact: │          │
│         │  │Reports:2│ │Reports:3│ │Reports:1│          │
│         │  └─────────┘ └─────────┘ └─────────┘          │
│         │  ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│         │  │  More   │ │  Cards  │ │   ...   │          │
└──────────────────────────────────────────────────────────┘
```

**Key Elements**:
- Search bar at top
- Grid of patient cards
- Each card shows: avatar, name, details
- Hover effects on cards

**Colors**:
- Cards: White with blue border on hover
- Avatar: Blue gradient circle
- Text: Dark blue headings, gray details

---

## 4. 📝 Reports Page

**URL**: `/reports/`

**Layout**:
```
┌──────────────────────────────────────────────────────────┐
│ SIDEBAR │  HEADER: Medical Reports                       │
│         │  View and manage all medical reports           │
├─────────┼────────────────────────────────────────────────┤
│         │  [Status:All▼] [Search:_______] [Filter]      │
│         │                                                │
│         │  REPORTS TABLE                                │
│         │  Report ID│Patient │Date    │Status │AI│Action│
│         │  ─────────┼────────┼────────┼───────┼──┼──────│
│         │  REP-067  │John Doe│04-12   │🟢Normal│✓│[View]│
│         │  REP-066  │Sarah   │04-11   │🟡Risk │✓│[View]│
│         │  REP-065  │Robert  │04-10   │🔴Crit │✓│[View]│
│         │  REP-064  │Emily   │04-09   │🟢Normal│✓│[View]│
│         │  REP-063  │Michael │04-08   │🟢Normal│✓│[View]│
│         │  ...more rows...                              │
└──────────────────────────────────────────────────────────┘
```

**Key Elements**:
- Filter dropdown and search
- Table with all reports
- Status badges (color-coded)
- AI indicator badges
- View button for each report

**Colors**:
- Table header: Light gray background
- Status badges: Green/Orange/Red
- AI badge: Light blue

---

## 5. 📄 Report Detail Page

**URL**: `/reports/<report-id>/`

**Layout**:
```
┌──────────────────────────────────────────────────────────┐
│ SIDEBAR │  HEADER: Report Details                        │
├─────────┼────────────────────────────────────────────────┤
│         │  ┌────────────────────────────────────────────┐│
│         │  │ Report REP-067        🟢 Normal Status    ││
│         │  │ 📅 Apr 12, 2024  🕐 10:30 AM              ││
│         │  │ 🤖 AI Generated Report                    ││
│         │  ├────────────────────────────────────────────┤│
│         │  │ 👤 PATIENT INFORMATION                    ││
│         │  │ Name: John Doe      Age: 45 years        ││
│         │  │ Gender: Male        Contact: 1234567890  ││
│         │  └────────────────────────────────────────────┘│
│         │                                                │
│         │  ┌────────────────────────────────────────────┐│
│         │  │ 📋 REPORT CONTENT                         ││
│         │  │ Medical examination report for John Doe.  ││
│         │  │ Patient presented with routine checkup... ││
│         │  └────────────────────────────────────────────┘│
│         │                                                │
│         │  ┌────────────────────────────────────────────┐│
│         │  │ 🩺 DIAGNOSIS                              ││
│         │  │ Normal health indicators. All vital      ││
│         │  │ signs within acceptable range...         ││
│         │  └────────────────────────────────────────────┘│
│         │                                                │
│         │  ┌────────────────────────────────────────────┐│
│         │  │ 📝 RECOMMENDATIONS                        ││
│         │  │ Continue regular health maintenance.     ││
│         │  │ Follow-up in 6 months...                 ││
│         │  └────────────────────────────────────────────┘│
│         │                                                │
│         │  [← Back to Reports] [🖨️ Print Report]       │
└──────────────────────────────────────────────────────────┘
```

**Key Elements**:
- Report header with ID and status
- Patient information section
- Report content box
- Diagnosis section
- Recommendations section
- Action buttons (back, print)

**Colors**:
- Sections: White cards with gray borders
- Content boxes: Light gray background
- Buttons: Gray and blue

---

## 6. 🤖 AI Analysis Page

**URL**: `/ai-analysis/`

**Layout**:
```
┌──────────────────────────────────────────────────────────┐
│ SIDEBAR │  HEADER: AI Analysis                           │
├─────────┼────────────────────────────────────────────────┤
│         │  STATS (3 boxes)                               │
│         │  ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│         │  │   67    │ │    2    │ │   85%   │          │
│         │  │ Total AI│ │Critical │ │ Normal  │          │
│         │  │ Reports │ │  Cases  │ │  Rate   │          │
│         │  └─────────┘ └─────────┘ └─────────┘          │
│         │                                                │
│         │  ┌──────────┐  ┌────────────────────────────┐ │
│         │  │📊 Status │  │🤖 AI-GENERATED REPORTS    │ │
│         │  │Distribution│  │                           │ │
│         │  │          │  │ ┌───────────────────────┐ │ │
│         │  │   🥧    │  │ │REP-067  🟢Normal     │ │ │
│         │  │  Donut  │  │ │👤 John Doe 📅 Apr 12 │ │ │
│         │  │  Chart  │  │ │[View Report]         │ │ │
│         │  │          │  │ └───────────────────────┘ │ │
│         │  │Normal 10 │  │ ┌───────────────────────┐ │ │
│         │  │At Risk 3│  │ │REP-066  🟡At Risk    │ │ │
│         │  │Critical 2│  │ │👤 Sarah 📅 Apr 11    │ │ │
│         │  │          │  │ │[View Report]         │ │ │
│         │  └──────────┘  │ └───────────────────────┘ │ │
│         │                │ ...more reports...         │ │
└──────────────────────────────────────────────────────────┘
```

**Key Elements**:
- 3 statistics boxes at top
- Donut chart with status distribution
- Legend with color indicators
- List of AI-generated reports
- Report cards with quick view

**Colors**:
- Stat boxes: Purple/Pink/Cyan gradients
- Chart: Green/Orange/Red segments
- Report cards: White with borders

---

## 🎨 Design System Summary

### Typography
- **Headings**: 'Segoe UI', sans-serif
- **Body**: 'Segoe UI', sans-serif
- **Sizes**: 11px-42px range

### Color Palette
```
Primary Colors:
- Blue: #1e3a8a (dark), #3b82f6 (normal), #60a5fa (light)
- Purple: #667eea to #764ba2 (gradient)

Status Colors:
- Success/Normal: #10b981 (green)
- Warning/At Risk: #f59e0b (orange)
- Danger/Critical: #ef4444 (red)

Neutral Colors:
- Background: #f5f6fa
- White: #ffffff
- Gray 100: #f9fafb
- Gray 200: #e5e7eb
- Gray 600: #6b7280
- Gray 900: #1e3a8a
```

### Component Styles

**Cards**:
- Background: White
- Border-radius: 12px
- Shadow: 0 2px 8px rgba(0,0,0,0.08)
- Padding: 24px

**Buttons**:
- Primary: Gradient purple background
- Secondary: Gray background
- Border-radius: 8px
- Hover: Slight lift effect

**Badges**:
- Border-radius: 12px
- Padding: 5px 14px
- Font-size: 12px
- Font-weight: 600

**Sidebar**:
- Width: 250px
- Fixed position
- Blue gradient background
- White text

### Responsive Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

---

## 📱 Mobile Responsive Features

All pages adapt to smaller screens:
- Sidebar collapses or becomes overlay
- Grid layouts become single column
- Tables scroll horizontally
- Touch-friendly button sizes
- Optimized spacing

---

This guide helps you understand the visual structure of each page in the MediGenAI application!
