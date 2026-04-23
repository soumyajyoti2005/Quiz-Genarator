<svg viewBox="0 0 900 280" xmlns="http://www.w3.org/2000/svg" width="900" height="280">
  <defs>
    <!-- Deep space background gradient -->
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%"   stop-color="#07080f"/>
      <stop offset="50%"  stop-color="#0d0f1e"/>
      <stop offset="100%" stop-color="#0b0e1b"/>
    </linearGradient>

    <!-- Indigo aurora -->
    <radialGradient id="aurora1" cx="20%" cy="20%" r="55%">
      <stop offset="0%"   stop-color="#6366f1" stop-opacity="0.30"/>
      <stop offset="100%" stop-color="#6366f1" stop-opacity="0"/>
    </radialGradient>

    <!-- Pink aurora -->
    <radialGradient id="aurora2" cx="85%" cy="80%" r="50%">
      <stop offset="0%"   stop-color="#ec4899" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#ec4899" stop-opacity="0"/>
    </radialGradient>

    <!-- Emerald aurora -->
    <radialGradient id="aurora3" cx="55%" cy="50%" r="40%">
      <stop offset="0%"   stop-color="#10b981" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#10b981" stop-opacity="0"/>
    </radialGradient>

    <!-- Title gradient -->
    <linearGradient id="titleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"   stop-color="#a5b4fc"/>
      <stop offset="50%"  stop-color="#c084fc"/>
      <stop offset="100%" stop-color="#f9a8d4"/>
    </linearGradient>

    <!-- Orb glow -->
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>

    <filter id="softglow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <!-- Clip -->
    <clipPath id="clip">
      <rect width="900" height="280" rx="20"/>
    </clipPath>
  </defs>

  <g clip-path="url(#clip)">
    <!-- Background -->
    <rect width="900" height="280" fill="url(#bg)" rx="20"/>

    <!-- Aurora layers -->
    <rect width="900" height="280" fill="url(#aurora1)"/>
    <rect width="900" height="280" fill="url(#aurora2)"/>
    <rect width="900" height="280" fill="url(#aurora3)"/>

    <!-- Stars -->
    <circle cx="54"  cy="30"  r="1.2" fill="white" opacity="0.55"/>
    <circle cx="130" cy="18"  r="0.8" fill="white" opacity="0.40"/>
    <circle cx="210" cy="55"  r="1.0" fill="white" opacity="0.50"/>
    <circle cx="320" cy="22"  r="1.3" fill="white" opacity="0.45"/>
    <circle cx="440" cy="40"  r="0.9" fill="white" opacity="0.35"/>
    <circle cx="560" cy="15"  r="1.1" fill="white" opacity="0.55"/>
    <circle cx="650" cy="48"  r="0.7" fill="white" opacity="0.40"/>
    <circle cx="740" cy="25"  r="1.2" fill="white" opacity="0.50"/>
    <circle cx="820" cy="60"  r="0.8" fill="white" opacity="0.35"/>
    <circle cx="870" cy="20"  r="1.0" fill="white" opacity="0.45"/>
    <circle cx="80"  cy="230" r="0.9" fill="white" opacity="0.30"/>
    <circle cx="180" cy="250" r="1.1" fill="white" opacity="0.40"/>
    <circle cx="290" cy="240" r="0.7" fill="white" opacity="0.35"/>
    <circle cx="700" cy="235" r="1.0" fill="white" opacity="0.40"/>
    <circle cx="800" cy="255" r="0.8" fill="white" opacity="0.30"/>
    <circle cx="860" cy="240" r="1.2" fill="white" opacity="0.45"/>
    <circle cx="25"  cy="140" r="0.8" fill="white" opacity="0.35"/>
    <circle cx="875" cy="130" r="0.9" fill="white" opacity="0.40"/>

    <!-- Decorative orb blobs (blurred) -->
    <circle cx="120" cy="80"  r="70" fill="#6366f1" opacity="0.10" filter="url(#softglow)"/>
    <circle cx="780" cy="200" r="80" fill="#ec4899" opacity="0.09" filter="url(#softglow)"/>

    <!-- Floating quiz symbols (left side) -->
    <text x="38" y="120" font-size="32" fill="white" opacity="0.08" font-family="serif">∑</text>
    <text x="22" y="195" font-size="26" fill="white" opacity="0.07" font-family="serif">π</text>
    <text x="48" y="255" font-size="22" fill="white" opacity="0.06" font-family="serif">∞</text>

    <!-- Floating quiz symbols (right side) -->
    <text x="840" cy="80"  y="100" font-size="30" fill="white" opacity="0.08" font-family="serif">?</text>
    <text x="855" y="170" font-size="24" fill="white" opacity="0.07" font-family="serif">√</text>
    <text x="838" y="240" font-size="22" fill="white" opacity="0.06" font-family="serif">∫</text>

    <!-- Glowing orb accent top-left -->
    <circle cx="90" cy="75" r="4" fill="#a5b4fc" opacity="0.9" filter="url(#glow)"/>
    <circle cx="810" cy="200" r="3.5" fill="#f9a8d4" opacity="0.85" filter="url(#glow)"/>
    <circle cx="450" cy="30" r="3" fill="#6ee7b7" opacity="0.70" filter="url(#glow)"/>

    <!-- Thin top border line gradient -->
    <rect x="0" y="0" width="900" height="2" rx="1" fill="url(#titleGrad)" opacity="0.6"/>

    <!-- Crystal/gem icon -->
    <g transform="translate(390, 68)" filter="url(#glow)">
      <!-- Gem shape -->
      <polygon points="30,0 58,18 58,46 30,62 2,46 2,18" fill="none" stroke="url(#titleGrad)" stroke-width="1.5" opacity="0.8"/>
      <polygon points="30,0 58,18 30,30" fill="#a5b4fc" opacity="0.18"/>
      <polygon points="30,0 2,18 30,30"  fill="#c084fc" opacity="0.18"/>
      <polygon points="2,18 2,46 30,30"  fill="#6366f1" opacity="0.20"/>
      <polygon points="58,18 58,46 30,30" fill="#ec4899" opacity="0.18"/>
      <polygon points="2,46 30,62 30,30"  fill="#8b5cf6" opacity="0.20"/>
      <polygon points="58,46 30,62 30,30" fill="#c084fc" opacity="0.18"/>
      <!-- Inner sparkle -->
      <circle cx="30" cy="30" r="4" fill="white" opacity="0.55"/>
    </g>

    <!-- Main title -->
    <text
      x="450" y="172"
      text-anchor="middle"
      font-family="Georgia, 'Times New Roman', serif"
      font-size="62"
      font-weight="bold"
      letter-spacing="-1"
      fill="url(#titleGrad)"
    >QuizVerse</text>

    <!-- Subtitle -->
    <text
      x="450" y="202"
      text-anchor="middle"
      font-family="'Courier New', monospace"
      font-size="13"
      letter-spacing="5"
      fill="white"
      opacity="0.40"
    >✦  AI-POWERED QUIZ GENERATOR  ✦</text>

    <!-- Badges row -->
    <!-- Badge 1: Streamlit -->
    <rect x="270" y="224" width="100" height="26" rx="13" fill="#6366f1" opacity="0.25"/>
    <rect x="270" y="224" width="100" height="26" rx="13" fill="none" stroke="#6366f1" stroke-width="1" opacity="0.6"/>
    <text x="320" y="241" text-anchor="middle" font-family="monospace" font-size="11" fill="#a5b4fc" letter-spacing="1">⚡ Streamlit</text>

    <!-- Badge 2: Gemini -->
    <rect x="382" y="224" width="136" height="26" rx="13" fill="#ec4899" opacity="0.18"/>
    <rect x="382" y="224" width="136" height="26" rx="13" fill="none" stroke="#ec4899" stroke-width="1" opacity="0.5"/>
    <text x="450" y="241" text-anchor="middle" font-family="monospace" font-size="11" fill="#f9a8d4" letter-spacing="1">🤖 Gemini 2.5 Flash</text>

    <!-- Badge 3: Free -->
    <rect x="530" y="224" width="100" height="26" rx="13" fill="#10b981" opacity="0.18"/>
    <rect x="530" y="224" width="100" height="26" rx="13" fill="none" stroke="#10b981" stroke-width="1" opacity="0.5"/>
    <text x="580" y="241" text-anchor="middle" font-family="monospace" font-size="11" fill="#6ee7b7" letter-spacing="1">✨ Free Tier</text>

    <!-- Bottom border -->
    <rect x="0" y="278" width="900" height="2" rx="1" fill="url(#titleGrad)" opacity="0.3"/>
  </g>
</svg>
