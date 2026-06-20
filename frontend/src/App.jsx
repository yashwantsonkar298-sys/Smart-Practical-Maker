import { useState, useEffect } from 'react';

const API_BASE_URL = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');

export default function App() {
  const [text, setText] = useState('');
  const [fileName, setFileName] = useState('Data_Structures_Lab_File');
  const [imageUrl, setImageUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [successMsg, setSuccessMsg] = useState('');
  const [apiStatus, setApiStatus] = useState('checking');

  // --- ACADEMIC METADATA STATES ---
  const [studentName, setStudentName] = useState('');
  const [rollNo, setRollNo] = useState('');
  const [collegeName, setCollegeName] = useState('ABES Engineering College');
  const [subjectCode, setSubjectCode] = useState('');
  const [assignmentDate, setAssignmentDate] = useState(new Date().toISOString().split('T')[0]);

  // --- 🎯 NEW: HEADER POSITION CONTROLS ---
  const [headerX, setHeaderX] = useState(130); // Left/Right position
  const [headerY, setHeaderY] = useState(50);  // Up/Down position

  // --- ADVANCED CALIBRATION TOOLS ---
  const [fontSize, setFontSize] = useState(38); 
  const [lineGap, setLineGap] = useState(48);   
  const [marginLeft, setMarginLeft] = useState(130); 
  const [topMargin, setTopMargin] = useState(190); // 🎯 NEW: Top Crop/Margin 
  const [realismLevel, setRealismLevel] = useState(4); 

  // --- 🕵️‍♂️ ANTI-DETECTION STEALTH STATES ---
  const [stealthMode, setStealthMode] = useState(true); 
  const [inkSmudge, setInkSmudge] = useState(2);        
  const [pageShadows, setPageShadows] = useState(true); 

  // --- STYLE CONFIGURATIONS ---
  const [darkMode, setDarkMode] = useState(true); 
  const [pageStyle, setPageStyle] = useState('ruled'); 
  const [inkType, setInkType] = useState('blue');     
  const [fontProfile, setFontProfile] = useState('font_1'); 
  const [includePageNumbers, setIncludePageNumbers] = useState(true);
  const [includeLabHeader, setIncludeLabHeader] = useState(true); 

  const templates = {
    blank: "",
    cpp_basic: `#include <iostream>\nusing namespace std;\n\nint main() {\n    // Write your logic here\n    cout << "Hello World!" << endl;\n    return 0;\n}`,
    lab_experiment: `EXPERIMENT NO: 01\n\nAIM: To implement Binary Search Algorithm in C++ and analyze its time complexity.\n\nALGORITHM:\n1. Start with the entire array.\n2. If the search key is less than the item in the middle of the interval, narrow the interval to the lower half.\n3. Otherwise, narrow it to the upper half.\n4. Repeatedly check until the value is found or the interval is empty.\n\nCODE:\n#include <iostream>\nusing namespace std;\n// Insert Code Here\n\nOUTPUT:\nElement found at index 3\nTime Complexity: O(log n)`,
  };

  const pageIdByStyle = {
    ruled: 'page_1',
    blank: 'page_blank',
    grid: 'page_grid',
    abes_practical: 'page_abes_practical',
  };

  const fontProfileOptions = [
    { value: 'font_1', label: 'Font 1 - Casual (Alpha)' },
    { value: 'font_2', label: 'Font 2 - Neat (Beta)' },
    { value: 'font_3', label: 'Font 3 - Cursive (Gamma)' },
    { value: 'font_4', label: 'Font 4 - Messy (Delta)' },
    { value: 'font_5', label: 'Font 5 - Tiny (Epsilon)' },
    { value: 'font_6', label: 'Font 6 - Bold (Zeta)' },
    { value: 'font_7', label: 'Font 7 - Slanted (Eta)' },
    { value: 'font_8', label: 'Font 8 - Round (Theta)' },
    { value: 'font_9', label: 'Font 9 - Sharp (Iota)' },
    { value: 'font_10', label: 'Font 10 - Doctors (Kappa)' },
    { value: 'vani', label: 'Vani - Same Photo Style' },
    { value: 'photo_1', label: '1 - Photo Rounded Casual' },
    { value: 'photo_2', label: '2 - Photo Neat Print' },
    { value: 'photo_3', label: '3 - Photo Compact Cursive' },
    { value: 'photo_4', label: '4 - Photo Slanted Cursive' },
    { value: 'photo_6', label: '6 - Photo Dark Cursive' },
    { value: 'photo_7', label: '7 - Photo Flow Cursive' },
  ];

  const photoProfilePresets = {
    vani: { fontSize: 36, lineGap: 48, realism: 5, ink: 'blue', smudge: 1 },
    photo_1: { fontSize: 36, lineGap: 48, realism: 5, ink: 'blue', smudge: 1 },
    photo_2: { fontSize: 35, lineGap: 46, realism: 3, ink: 'blue', smudge: 1 },
    photo_3: { fontSize: 34, lineGap: 45, realism: 2, ink: 'black', smudge: 1 },
    photo_4: { fontSize: 36, lineGap: 50, realism: 2, ink: 'blue', smudge: 1 },
    photo_6: { fontSize: 37, lineGap: 51, realism: 3, ink: 'black', smudge: 2 },
    photo_7: { fontSize: 35, lineGap: 49, realism: 2, ink: 'blue', smudge: 1 },
  };

  const applyTemplate = (templateKey) => {
    if (text.trim() && !window.confirm("Aapka current text delete ho jayega. Load karein?")) return;
    setText(templates[templateKey]);
  };

  const applyFontProfile = (profileId) => {
    setFontProfile(profileId);
    const preset = photoProfilePresets[profileId];
    if (!preset) return;

    setFontSize(preset.fontSize);
    setLineGap(preset.lineGap);
    setRealismLevel(preset.realism);
    setInkType(preset.ink);
    setInkSmudge(preset.smudge);
  };

  const charCount = text.length;
  const wordCount = text.trim() === '' ? 0 : text.trim().split(/\s+/).length;
  const lineCount = text.split('\n').length;
  const estimatedPages = Math.max(1, Math.ceil(lineCount / 30));

  useEffect(() => {
    if (darkMode) document.documentElement.classList.add('dark');
    else document.documentElement.classList.remove('dark');
  }, [darkMode]);

  useEffect(() => {
    let cancelled = false;

    fetch(`${API_BASE_URL}/health`)
      .then((response) => {
        if (!response.ok) throw new Error('Health check failed');
        if (!cancelled) setApiStatus('online');
      })
      .catch(() => {
        if (!cancelled) setApiStatus('offline');
      });

    return () => {
      cancelled = true;
    };
  }, []);

  const executeAiEngine = async () => {
    if (!text.trim()) {
      showError("Error: Textarea khali hai! Pehle assignment ka content ya C++ code daalo.");
      return;
    }
    setLoading(true); setError(null); setSuccessMsg('');

    try {
      const payload = {
        text: text,
        font_id: fontProfile, 
        page_id: pageIdByStyle[pageStyle] || 'page_1', 
        ink_color: inkType,
        student_name: studentName,
        roll_number: rollNo,
        college_name: collegeName,
        subject_code: subjectCode,
        date: assignmentDate,
        page_numbering: includePageNumbers,
        lab_header: includeLabHeader,
        font_size: fontSize,
        line_gap: lineGap,
        margin_left: marginLeft,
        top_margin: topMargin,   // Sending Top Margin
        header_x: headerX,       // Sending Header X
        header_y: headerY,       // Sending Header Y
        realism_factor: realismLevel,
        stealth_scanner_effect: stealthMode,
        ink_smudge_level: inkSmudge,
        uneven_lighting: pageShadows
      };

      const response = await fetch(`${API_BASE_URL}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        let message = "Server pipeline connection failed.";
        try {
          const data = await response.json();
          message = data.detail || message;
        } catch {
          message = `${message} Status ${response.status}`;
        }
        throw new Error(message);
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      setImageUrl(url);
      setSuccessMsg("Print-Ready Stealth PDF Compiled Successfully! 🕵️‍♂️🎉");
      setTimeout(() => setSuccessMsg(''), 4000);
    } catch (err) {
      showError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const showError = (msg) => { setError(msg); setTimeout(() => setError(null), 4000); };

  return (
    <div className={`app-shell min-h-screen transition-colors duration-700 font-sans selection:bg-blue-500/30 flex flex-col items-center ${darkMode ? 'theme-dark text-gray-100' : 'theme-light text-slate-900'}`}>
      
      {/* NAVBAR */}
      <nav className={`workspace-nav w-full fixed top-0 z-50 backdrop-blur-2xl border-b transition-all duration-500 flex justify-center ${darkMode ? 'bg-[#0B0F19]/80 border-gray-800' : 'bg-white/70 border-gray-200 shadow-sm'}`}>
        <div className="w-full max-w-7xl px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <div className="brand-mark w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo-600 to-cyan-500 flex items-center justify-center shadow-lg shadow-blue-500/20 ring-2 ring-white/10">
              <span className="text-2xl">🕵️‍♂️</span>
            </div>
            <div>
              <h1 className="text-2xl font-black tracking-tight leading-none">Smart Practical <span className="text-transparent bg-clip-text bg-gradient-to-r from-red-500 to-orange-500">Stealth</span></h1>
              <span className="text-[10px] font-bold uppercase tracking-widest text-red-500 mt-1">Anti-Detection Print Edition V5.0</span>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className={`hidden sm:inline-flex items-center gap-2 rounded-full border px-3 py-2 text-[11px] font-black uppercase tracking-wider ${apiStatus === 'online' ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-400' : apiStatus === 'offline' ? 'border-red-500/30 bg-red-500/10 text-red-400' : 'border-amber-500/30 bg-amber-500/10 text-amber-400'}`}>
              <span className={`h-2 w-2 rounded-full ${apiStatus === 'online' ? 'bg-emerald-400' : apiStatus === 'offline' ? 'bg-red-400' : 'bg-amber-400'}`}></span>
              API {apiStatus}
            </span>
            <button onClick={() => setDarkMode(!darkMode)} className={`p-3 rounded-full border transition-all ${darkMode ? 'bg-gray-800 border-gray-700 text-yellow-400' : 'bg-gray-100 border-gray-200 text-indigo-600'}`}>
              {darkMode ? '☀️ Light' : '🌙 Dark'}
            </button>
          </div>
        </div>
      </nav>

      {/* MAIN WORKSPACE */}
      <main className="workspace-main pt-32 pb-20 w-full max-w-[1400px] px-4 flex flex-col items-center">
        
        {/* METADATA & CONTROL PANEL */}
        <div className={`professional-panel w-full max-w-6xl p-6 rounded-3xl mb-6 border backdrop-blur-md shadow-2xl ${darkMode ? 'bg-gray-900/60 border-gray-800' : 'bg-white border-gray-200'}`}>
          
          <div className="control-section control-section-warm p-4 mb-6 rounded-2xl bg-gradient-to-r from-red-500/10 to-orange-500/10 border border-red-500/20">
            <h3 className="text-xs font-black uppercase tracking-widest mb-4 text-red-500 flex items-center gap-2">
              <span>⚠️</span> Anti-Detection Print Setup
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 items-center">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-bold uppercase tracking-wider opacity-80">CamScanner Effect</span>
                <button onClick={() => setStealthMode(!stealthMode)} className={`w-12 h-6 rounded-full transition-colors ${stealthMode ? 'bg-red-500' : 'bg-gray-600'} relative`}><span className={`absolute top-1 left-1 bg-white w-4 h-4 rounded-full transition-transform ${stealthMode ? 'translate-x-6' : ''}`}></span></button>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-bold uppercase tracking-wider opacity-80">Uneven Shadows</span>
                <button onClick={() => setPageShadows(!pageShadows)} className={`w-12 h-6 rounded-full transition-colors ${pageShadows ? 'bg-red-500' : 'bg-gray-600'} relative`}><span className={`absolute top-1 left-1 bg-white w-4 h-4 rounded-full transition-transform ${pageShadows ? 'translate-x-6' : ''}`}></span></button>
              </div>
              <div>
                <div className="flex justify-between text-[11px] font-bold uppercase tracking-wider opacity-80 mb-1"><span>Ink Smudge</span> <span className="text-red-400">Lvl {inkSmudge}</span></div>
                <input type="range" min="0" max="5" value={inkSmudge} onChange={(e) => setInkSmudge(Number(e.target.value))} className="w-full accent-red-500" />
              </div>
            </div>
          </div>

          {/* 🎯 NEW: Header Placement Sliders */}
          <h3 className="text-xs font-black uppercase tracking-widest mb-3 text-purple-500 flex items-center gap-2 pt-2">
            <span>📍</span> Header Details & Custom Placement
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4 mb-4">
            <input type="text" value={studentName} onChange={(e) => setStudentName(e.target.value)} className={`w-full px-4 py-2 rounded-xl border text-sm font-semibold outline-none ${darkMode ? 'bg-gray-950 border-gray-800' : 'bg-gray-50 border-gray-300'}`} placeholder="Name..." />
            <input type="text" value={rollNo} onChange={(e) => setRollNo(e.target.value)} className={`w-full px-4 py-2 rounded-xl border text-sm font-semibold outline-none ${darkMode ? 'bg-gray-950 border-gray-800' : 'bg-gray-50 border-gray-300'}`} placeholder="Roll No..." />
            <input type="text" value={collegeName} onChange={(e) => setCollegeName(e.target.value)} className={`w-full px-4 py-2 rounded-xl border text-sm font-semibold outline-none ${darkMode ? 'bg-gray-950 border-gray-800' : 'bg-gray-50 border-gray-300'}`} placeholder="College..." />
            <input type="text" value={subjectCode} onChange={(e) => setSubjectCode(e.target.value)} className={`w-full px-4 py-2 rounded-xl border text-sm font-semibold outline-none ${darkMode ? 'bg-gray-950 border-gray-800' : 'bg-gray-50 border-gray-300'}`} placeholder="Subject..." />
            <input type="date" value={assignmentDate} onChange={(e) => setAssignmentDate(e.target.value)} className={`w-full px-4 py-2 rounded-xl border text-sm font-semibold outline-none ${darkMode ? 'bg-gray-950 border-gray-800' : 'bg-gray-50 border-gray-300'}`} />
          </div>
          
          <div className="control-section control-section-violet grid grid-cols-1 sm:grid-cols-2 gap-6 mb-6 px-2 bg-purple-500/5 p-4 rounded-xl border border-purple-500/20">
            <div>
              <div className="flex justify-between text-[11px] font-bold uppercase tracking-wider text-purple-400 mb-1"><span>Name/Roll Left-Right (X Position)</span><span>{headerX}px</span></div>
              <input type="range" min="10" max="800" value={headerX} onChange={(e) => setHeaderX(Number(e.target.value))} className="w-full accent-purple-500" />
            </div>
            <div>
              <div className="flex justify-between text-[11px] font-bold uppercase tracking-wider text-purple-400 mb-1"><span>Name/Roll Up-Down (Y Position)</span><span>{headerY}px</span></div>
              <input type="range" min="10" max="500" value={headerY} onChange={(e) => setHeaderY(Number(e.target.value))} className="w-full accent-purple-500" />
            </div>
          </div>

          <h3 className="text-xs font-black uppercase tracking-widest mb-3 text-cyan-500 flex items-center gap-2 pt-2 border-t border-gray-500/10">
            <span>🎛️</span> Layout & Text Calibration
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4 mb-6">
            <div>
              <div className="flex justify-between text-[11px] font-bold uppercase opacity-70 mb-1"><span>Font Size</span><span>{fontSize}px</span></div>
              <input type="range" min="25" max="60" value={fontSize} onChange={(e) => setFontSize(Number(e.target.value))} className="w-full accent-cyan-500" />
            </div>
            <div>
              <div className="flex justify-between text-[11px] font-bold uppercase opacity-70 mb-1"><span>Line Gap</span><span>{lineGap}px</span></div>
              <input type="range" min="30" max="70" value={lineGap} onChange={(e) => setLineGap(Number(e.target.value))} className="w-full accent-cyan-500" />
            </div>
            <div>
              <div className="flex justify-between text-[11px] font-bold uppercase opacity-70 mb-1"><span>Left Margin</span><span>{marginLeft}px</span></div>
              <input type="range" min="50" max="400" value={marginLeft} onChange={(e) => setMarginLeft(Number(e.target.value))} className="w-full accent-cyan-500" />
            </div>
            {/* 🎯 NEW: Top Margin / Crop Adjuster */}
            <div>
              <div className="flex justify-between text-[11px] font-bold uppercase opacity-70 mb-1 text-cyan-400"><span>Top Margin</span><span>{topMargin}px</span></div>
              <input type="range" min="50" max="500" value={topMargin} onChange={(e) => setTopMargin(Number(e.target.value))} className="w-full accent-cyan-500" />
            </div>
            <div>
              <div className="flex justify-between text-[11px] font-bold uppercase opacity-70 mb-1"><span>Shaking</span><span>{realismLevel}x</span></div>
              <input type="range" min="0" max="6" value={realismLevel} onChange={(e) => setRealismLevel(Number(e.target.value))} className="w-full accent-cyan-500" />
            </div>
          </div>

          <h3 className="text-xs font-black uppercase tracking-widest mb-3 text-indigo-500 flex items-center gap-2 pt-4 border-t border-gray-500/10">
            <span>⚙️</span> Formatting & Sheet Styles
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 items-end">
            <div>
              <label className="text-[11px] font-bold uppercase opacity-70 mb-1 block">File Name</label>
              <input type="text" value={fileName} onChange={(e) => setFileName(e.target.value)} className={`w-full px-4 py-2 rounded-xl border text-sm font-semibold outline-none ${darkMode ? 'bg-gray-950 border-gray-800' : 'bg-gray-50 border-gray-300'}`} />
            </div>
            <div>
              <label className="text-[11px] font-bold uppercase opacity-70 mb-1 block">Paper Base</label>
              <select value={pageStyle} onChange={(e) => setPageStyle(e.target.value)} className={`w-full px-4 py-2 rounded-xl border text-sm font-bold outline-none ${darkMode ? 'bg-gray-950 border-gray-800' : 'bg-gray-50 border-gray-300'}`}>
                <option value="ruled">Ruled Notebook</option>
                <option value="blank">Plain White</option>
                <option value="grid">Graph Grid</option>
                <option value="abes_practical">ABES Practical Sheet</option>
              </select>
            </div>
            {/* 🎯 NEW: 10 Handwriting Profiles */}
            <div>
              <label className="text-[11px] font-bold uppercase text-indigo-400 mb-1 block">Handwriting Profile + Photo Styles</label>
              <select value={fontProfile} onChange={(e) => applyFontProfile(e.target.value)} className={`w-full px-4 py-2 rounded-xl border text-sm font-bold outline-none ${darkMode ? 'bg-gray-950 border-gray-800' : 'bg-gray-50 border-gray-300'}`}>
                {fontProfileOptions.map((profile) => (
                  <option key={profile.value} value={profile.value}>{profile.label}</option>
                ))}
              </select>
            </div>
            <div className="flex items-center justify-around h-10 border rounded-xl px-2 shadow-inner border-gray-500/10">
              <button onClick={() => setInkType('blue')} className={`w-6 h-6 rounded-full bg-blue-600 border-2 transition-all ${inkType === 'blue' ? 'border-white scale-110 shadow-md' : 'border-transparent opacity-50'}`}></button>
              <button onClick={() => setInkType('black')} className={`w-6 h-6 rounded-full bg-slate-900 border-2 transition-all ${inkType === 'black' ? 'border-gray-400 scale-110' : 'border-transparent opacity-50'}`}></button>
              <button onClick={() => setInkType('pencil')} title="Pencil ink" className={`w-6 h-6 rounded-full bg-gray-400 border-2 transition-all ${inkType === 'pencil' ? 'border-white scale-110 shadow-md' : 'border-transparent opacity-50'}`}></button>
              <button onClick={() => setIncludePageNumbers(!includePageNumbers)} className={`text-[10px] font-black px-2 py-1 rounded-md border ${includePageNumbers ? 'bg-blue-600 border-transparent text-white' : 'opacity-40 text-gray-400 border-gray-500'}`}>P.NO</button>
              <button onClick={() => setIncludeLabHeader(!includeLabHeader)} className={`text-[10px] font-black px-2 py-1 rounded-md border ${includeLabHeader ? 'bg-cyan-600 border-transparent text-white' : 'opacity-40 text-gray-400 border-gray-500'}`}>HDR</button>
            </div>
          </div>
        </div>

        <div className="w-full max-w-6xl grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
          <div className="flex flex-col w-full space-y-4">
            <div className={`tool-strip p-3 rounded-2xl border flex flex-wrap items-center gap-2 ${darkMode ? 'bg-gray-900/40 border-gray-800' : 'bg-white border-gray-200 shadow-sm'}`}>
              <span className="text-xs font-bold uppercase opacity-60 ml-2">⚡ Quick Inject:</span>
              <button onClick={() => applyTemplate('cpp_basic')} className="px-3 py-1.5 rounded-xl text-xs font-bold bg-blue-500/10 text-blue-500 hover:bg-blue-500/20">C++ Boilerplate</button>
              <button onClick={() => applyTemplate('lab_experiment')} className="px-3 py-1.5 rounded-xl text-xs font-bold bg-indigo-500/10 text-indigo-500 hover:bg-indigo-500/20">Lab Experiment</button>
              <span className="text-[11px] font-bold uppercase opacity-50 ml-auto">{wordCount} Words | {charCount} Chars | ~{estimatedPages} Pages</span>
            </div>
            <div className={`editor-panel flex flex-col w-full h-[580px] rounded-3xl border shadow-2xl overflow-hidden ${darkMode ? 'bg-[#0F1423] border-gray-800' : 'bg-white border-gray-300'}`}>
              <div className={`editor-header flex items-center px-6 py-4 border-b ${darkMode ? 'bg-[#151B2B] border-gray-800' : 'bg-gray-100 border-gray-200'}`}>
                <span className="text-sm font-mono font-black tracking-widest text-indigo-400">INPUT_WORKSPACE.cpp</span>
              </div>
              <textarea className={`editor-textarea w-full flex-1 p-6 focus:outline-none text-[16px] resize-none font-mono leading-loose ${darkMode ? 'bg-[#0F1423] text-blue-300 caret-white' : 'bg-white text-slate-800 caret-black'}`} placeholder="// Type or paste your assignments/code here..." value={text} onChange={(e) => setText(e.target.value)} spellCheck="false"></textarea>
              <div className={`p-4 border-t ${darkMode ? 'bg-[#151B2B] border-gray-800' : 'bg-gray-50 border-gray-200'}`}>
                <button onClick={executeAiEngine} disabled={loading} className={`primary-action w-full flex justify-center items-center gap-3 py-5 rounded-2xl font-black text-xl uppercase tracking-widest transition-all duration-300 shadow-xl ${loading ? 'bg-gray-600 cursor-not-allowed text-gray-300' : 'bg-gradient-to-r from-red-600 to-orange-600 text-white hover:-translate-y-1'}`}>
                  {loading ? 'Processing Stealth PDF...' : 'Compile Print-Ready PDF 🚀'}
                </button>
              </div>
            </div>
          </div>
          <div className={`preview-panel flex flex-col w-full h-[644px] rounded-3xl border-2 border-dashed p-6 transition-all duration-500 items-center justify-center relative overflow-hidden ${darkMode ? 'border-gray-800 bg-[#0B0F19]/50' : 'border-gray-300 bg-gray-50'}`}>
            {imageUrl ? (
              <div className="w-full h-full flex flex-col items-center justify-between animate-fade-in z-10 space-y-4">
                <div className="pdf-frame w-full flex-1 rounded-2xl overflow-hidden shadow-2xl ring-1 ring-white/10 bg-white">
                  <iframe src={`${imageUrl}#toolbar=0`} title="Academic Assignment Result" className="w-full h-full border-none" />
                </div>
                <a href={imageUrl} download={`${fileName}.pdf`} className="download-action w-full flex items-center justify-center gap-3 bg-red-500 hover:bg-red-400 text-white font-black text-lg py-4 px-6 rounded-2xl shadow-xl transition-all hover:-translate-y-1 uppercase tracking-widest">
                  Download Stealth PDF
                </a>
              </div>
            ) : (
              <div className="text-center z-10 flex flex-col items-center opacity-60">
                <div className="w-24 h-24 rounded-full flex items-center justify-center mb-4 bg-red-500/10"><span className="text-4xl">🖨️</span></div>
                <h3 className="text-2xl font-black mb-2 tracking-tight">System Standby</h3>
                <p className="text-sm max-w-sm font-medium">Turn on Stealth features to generate a PDF that looks 100% like a scanned handwritten document.</p>
              </div>
            )}
          </div>
        </div>
      </main>
      {error && <div className="fixed bottom-10 left-1/2 -translate-x-1/2 bg-red-600 text-white px-8 py-4 rounded-2xl shadow-2xl font-bold z-50">⚠️ {error}</div>}
      {successMsg && <div className="fixed bottom-10 left-1/2 -translate-x-1/2 bg-green-500 text-white px-8 py-4 rounded-2xl shadow-2xl font-bold z-50">✅ {successMsg}</div>}
    </div>
  );
}
