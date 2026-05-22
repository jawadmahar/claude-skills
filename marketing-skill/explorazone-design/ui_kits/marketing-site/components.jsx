/* =========================================================
   marketing-site UI kit components
   Loaded via Babel; components attached to window.
   ========================================================= */

const LOGO_ORANGE = "../../assets/logos/explorazone-orange.png";
const LOGO_WHITE  = "../../assets/logos/explorazone-white.png";
const EMBLEM_WHITE_BG = "../../assets/logos/emblem-pattern-only.svg";
const EMBLEM_ORANGE_SQUARE = "../../assets/logos/emblem-orange-square.svg";

// ---------------------------------------------------------
// ContinuityBar (top of every page during dual-branding)
// ---------------------------------------------------------
function ContinuityBar() {
  return (
    <div className="mk-topbar">
      <span className="mk-formerly">★ Formerly Exploring Science &middot; new name, same team</span>
      <span className="mk-meta">
        <span>Open today 10:00 - 17:00</span>
        <span>01603 927900</span>
      </span>
    </div>
  );
}

// ---------------------------------------------------------
// Header
// ---------------------------------------------------------
function Header({ current = "home" }) {
  const items = [
    { id: "home",     label: "Visit",          href: "index.html" },
    { id: "tickets",  label: "Tickets",        href: "tickets.html" },
    { id: "schools",  label: "Schools",        href: "schools.html" },
    { id: "parties",  label: "Parties",        href: "#" },
    { id: "cafe",     label: "Cafe UFO",       href: "#" },
    { id: "whats-on", label: "What's On",      href: "#" },
  ];
  return (
    <header className="mk-header">
      <a href="index.html" aria-label="Explorazone home">
        <img className="mk-logo" src={LOGO_WHITE} alt="EXPLORAZONE - Science Discovery Lab" />
      </a>
      <nav className="mk-nav" aria-label="Primary">
        {items.map(it =>
          <a key={it.id} href={it.href} className={it.id === current ? "is-current" : ""}>{it.label}</a>
        )}
      </nav>
      <div className="mk-header-right">
        <a href="tickets.html" className="mk-btn primary sm">Book Tickets</a>
      </div>
    </header>
  );
}

// ---------------------------------------------------------
// Hero - orange field, headline, ledes, CTAs
// ---------------------------------------------------------
function Hero() {
  return (
    <section className="mk-hero mk-on-orange">
      <img src={EMBLEM_WHITE_BG} alt="" className="mk-hero-emblem" aria-hidden="true" />
      <div className="mk-hero-inner">
        <p className="mk-hero-eyebrow">Norwich &middot; NR5 9JA</p>
        <h1>15,000 Sq Ft of <span className="accent">Hands-on</span> Adventure.</h1>
        <p className="lede">80+ interactive exhibits, a VR zone, live workshops, and Cafe UFO on-site. Open seven days a week. Same team. New name. Bigger adventure.</p>
        <div className="mk-cta-row">
          <a href="tickets.html" className="mk-btn primary lg">Book a Visit</a>
          <a href="schools.html" className="mk-btn secondary lg">Plan a School Trip</a>
        </div>
      </div>
    </section>
  );
}

// ---------------------------------------------------------
// Stats strip - floating card under hero
// ---------------------------------------------------------
function Stats() {
  const data = [
    { n: "80+",      l: "Hands-on exhibits" },
    { n: "15,000",   l: "Square feet" },
    { n: "VR",       l: "Discovery zone" },
    { n: "7 days",   l: "Open all week" },
  ];
  return (
    <div className="mk-section tight" style={{paddingTop: 0, paddingBottom: 32}}>
      <div className="mk-stats">
        {data.map((s, i) =>
          <div key={i} className="mk-stat">
            <span className="n">{s.n}</span>
            <span className="l">{s.l}</span>
          </div>
        )}
      </div>
    </div>
  );
}

// ---------------------------------------------------------
// Section heading
// ---------------------------------------------------------
function SectionHead({ eyebrow, title, lede }) {
  return (
    <div className="mk-section-head">
      <div>
        {eyebrow && <p className="mk-eyebrow">{eyebrow}</p>}
        <h2>{title}</h2>
      </div>
      {lede && <p>{lede}</p>}
    </div>
  );
}

// ---------------------------------------------------------
// Attraction card
// ---------------------------------------------------------
function AttractionCard({ tag, title, desc, imgClass = "mk-img-1", placeholder = "Photo placeholder" }) {
  return (
    <article className="mk-card">
      <div className={`mk-card-img mk-img-placeholder ${imgClass}`} role="img" aria-label={placeholder}>
        <div className="mk-card-tag">{tag}</div>
        <span>{placeholder}</span>
      </div>
      <div className="mk-card-body">
        <h3>{title}</h3>
        <p>{desc}</p>
      </div>
      <div className="mk-card-foot">Find out more →</div>
    </article>
  );
}

// ---------------------------------------------------------
// Attractions grid
// ---------------------------------------------------------
function Attractions() {
  const items = [
    { tag: "Zone 1", imgClass: "mk-img-1", title: "Forces & Motion",      desc: "Pulleys, levers, ramps. Ten exhibits exploring the basic mechanics every curriculum touches.",   placeholder: "Forces hall photo" },
    { tag: "Zone 2", imgClass: "mk-img-3", title: "Sound & Light",        desc: "Build a beat, see a rainbow, look inside a thunderclap. Generous space for groups to spread out.", placeholder: "Sound lab photo" },
    { tag: "Zone 3", imgClass: "mk-img-2", title: "Human Body",           desc: "Heart pumps, skeleton puzzles, a giant ear you can walk inside. Bring a packed lunch.",            placeholder: "Body zone photo" },
    { tag: "Zone 4", imgClass: "mk-img-5", title: "VR Discovery",         desc: "Eight headsets, three guided experiences. Suitable from age 9. Pre-book your slot at the door.",   placeholder: "VR zone photo" },
    { tag: "Zone 5", imgClass: "mk-img-6", title: "Outdoor Workshops",    desc: "Weather-permitting demos in the courtyard. Rockets, slime, liquid nitrogen. Daily 14:00.",         placeholder: "Outdoor demo photo" },
    { tag: "Zone 6", imgClass: "mk-img-4", title: "Cafe UFO",             desc: "On-site cafe, kid menu from £4.50. Spaceship booths, retro arcade, hot drinks for grown-ups.",      placeholder: "Cafe UFO photo" },
  ];
  return (
    <section className="mk-section">
      <SectionHead
        eyebrow="What's inside"
        title="Six Zones. One Big Day Out."
        lede="Pick a zone or wander - the floor plan loops, so you can do it in any order. Allow 3-4 hours for a full visit." />
      <div className="mk-grid-3">
        {items.map((it, i) => <AttractionCard key={i} {...it} />)}
      </div>
    </section>
  );
}

// ---------------------------------------------------------
// Promo strip
// ---------------------------------------------------------
function PartiesPromo() {
  return (
    <section className="mk-promo mk-on-orange">
      <div className="mk-promo-inner">
        <div>
          <p className="mk-hero-eyebrow" style={{marginBottom: 8}}>For Birthdays</p>
          <h2>Party with a Bang.</h2>
          <p>Up to 20 guests, two hours of run-of-the-place, a private party room, and a science demo done loud. From £18 per child. No VAT. Cake optional, mess included.</p>
          <a className="mk-btn primary lg" href="#">See Party Options</a>
        </div>
        <div className="mk-promo-card">
          <p className="mk-eyebrow" style={{margin: 0}}>What's included</p>
          <h3 style={{fontFamily: "var(--ez-font-display)", textTransform: "uppercase", fontSize: 20, margin: "8px 0 14px", color: "var(--ez-fg)"}}>The Classic Party</h3>
          <ul style={{listStyle: "none", padding: 0, margin: 0, display: "flex", flexDirection: "column", gap: 8, fontSize: 14, color: "var(--ez-fg)"}}>
            <li><strong style={{color: "var(--ez-green-on-white)"}}>✓</strong> 90 min in the exhibit halls</li>
            <li><strong style={{color: "var(--ez-green-on-white)"}}>✓</strong> 30 min in a private party room</li>
            <li><strong style={{color: "var(--ez-green-on-white)"}}>✓</strong> A live science demo, picked by the birthday kid</li>
            <li><strong style={{color: "var(--ez-green-on-white)"}}>✓</strong> Goody bag + a thank-you card</li>
          </ul>
        </div>
      </div>
    </section>
  );
}

// ---------------------------------------------------------
// Schools strip
// ---------------------------------------------------------
function SchoolsPromo() {
  return (
    <section className="mk-section">
      <div className="mk-split">
        <div>
          <p className="mk-eyebrow">For Schools</p>
          <h2 style={{fontFamily: "var(--ez-font-display)", fontSize: "clamp(36px,4vw,56px)", lineHeight: 0.95, letterSpacing: "-0.02em", textTransform: "uppercase", color: "var(--ez-fg)", margin: "0 0 16px"}}>Curriculum-linked Trips That Actually Get Booked Again.</h2>
          <p style={{margin: 0, fontSize: 16, lineHeight: 1.6, color: "var(--ez-fg)", maxWidth: "54ch"}}>£18 per pupil, standard rate. Risk assessments, teacher prep packs, and SEND-friendly room maps included. Norfolk Short Breaks framework approved.</p>
          <div className="mk-quote">
            <p>"The team genuinely understood Year 4. They didn't talk down to the kids and the staff briefing was the best we've ever had."</p>
            <cite>Mrs Adeyemi, Bowthorpe Primary &middot; KS2 visit, March 2026</cite>
          </div>
          <a className="mk-btn primary" href="schools.html">Plan a Trip</a>
        </div>
        <ul className="mk-checklist" aria-label="Included with every school visit">
          <li>£18 pp standard rate, no add-on fees.</li>
          <li>Free coach parking and a quiet drop-off bay.</li>
          <li>Risk assessment template ready to download.</li>
          <li>Teacher prep pack mapped to Key Stages 1-3.</li>
          <li>SEND-friendly floor plan and a calm room on-site.</li>
          <li>One staff lead per 10 pupils, free of charge.</li>
        </ul>
      </div>
    </section>
  );
}

// ---------------------------------------------------------
// Footer
// ---------------------------------------------------------
function Footer() {
  return (
    <>
      <footer className="mk-footer">
        <div className="mk-footer-inner">
          <div>
            <img src={LOGO_WHITE} alt="EXPLORAZONE" className="mk-foot-logo" style={{background: "#fff", padding: "8px 12px", borderRadius: 8}} />
            <p style={{margin: "12px 0 4px", fontSize: 14, opacity: 0.85, maxWidth: "30ch"}}>Norwich's biggest interactive science centre. Operated by Coreaxis2 Ltd.</p>
            <p style={{margin: "0", fontSize: 12, opacity: 0.6}}>Formerly Exploring Science</p>
          </div>
          <div>
            <h4>Visit</h4>
            <a href="tickets.html">Tickets &amp; opening times</a>
            <a href="#">Getting here</a>
            <a href="#">Accessibility &amp; SEND</a>
            <a href="#">Frequently asked</a>
          </div>
          <div>
            <h4>Groups</h4>
            <a href="schools.html">School trips</a>
            <a href="#">Birthday parties</a>
            <a href="#">Holiday clubs</a>
            <a href="#">Private hire</a>
          </div>
          <div>
            <h4>About</h4>
            <a href="#">Our story</a>
            <a href="#">Cafe UFO</a>
            <a href="#">Press &amp; partners</a>
            <a href="#">Contact</a>
          </div>
        </div>
        <div className="mk-foot-meta">
          <span>Coreaxis2 Ltd &middot; Company No. 16929722 &middot; Unit 5-6, Francis Way, Bowthorpe Park, Norwich, NR5 9JA</span>
          <span>01603 927900 &middot; explorazone.co.uk</span>
        </div>
      </footer>
    </>
  );
}

// ---------------------------------------------------------
// Page shell - shared between index/tickets/schools
// ---------------------------------------------------------
function PageShell({ current, children }) {
  return (
    <>
      <ContinuityBar />
      <Header current={current} />
      {children}
      <Footer />
    </>
  );
}

// ---------------------------------------------------------
// Ticket card
// ---------------------------------------------------------
function TicketCard({ title, price, suffix = "per person", features = [], cta = "Book", featured = false }) {
  return (
    <article className={`mk-ticket${featured ? " featured" : ""}`}>
      <h3>{title}</h3>
      <div className="mk-price">£{price}<small> {suffix}</small></div>
      <ul>{features.map((f, i) => <li key={i}>{f}</li>)}</ul>
      <a className={`mk-btn ${featured ? "primary" : "secondary"}`}>{cta}</a>
    </article>
  );
}

// ---------------------------------------------------------
// BadgeStrip - sits below brand-coloured page hero
// ---------------------------------------------------------
function BadgeStrip({ items }) {
  return (
    <div className="mk-badge-strip" role="list">
      {items.map((t, i) =>
        <React.Fragment key={i}>
          {i > 0 && <span className="dot" aria-hidden="true"></span>}
          <span role="listitem">{t}</span>
        </React.Fragment>
      )}
    </div>
  );
}

// ---------------------------------------------------------
// TicketsPage
// ---------------------------------------------------------
function TicketsPage() {
  return (
    <>
      <section className="mk-page-hero brand">
        <img src={EMBLEM_WHITE_BG} alt="" className="mk-hero-emblem" aria-hidden="true" />
        <div className="mk-page-hero-inner" style={{position: "relative", zIndex: 2}}>
          <p className="mk-crumbs"><a href="index.html">Home</a> Tickets</p>
          <h1>Tickets &amp; Opening Times</h1>
          <p>Walk-ups welcome. Pre-booking saves time on busy weekends and during the school holidays. Same team, new name, bigger adventure.</p>
        </div>
      </section>
      <BadgeStrip items={[
        "Under 3s go free",
        "Free re-entry on the day",
        "Last entry 16:00",
        "Cafe UFO on-site",
      ]} />
      <section className="mk-section">
        <SectionHead
          eyebrow="General entry"
          title="Pick a Ticket."
          lede="All tickets include the full floor plan, daily live workshops, and the outdoor courtyard. VR zone is bookable on the day." />
        <div className="mk-ticket-grid">
          <TicketCard title="Child"       price="14" features={["Age 3-15", "Free re-entry on the day", "Daily live workshop"]} cta="Book Child Ticket" />
          <TicketCard title="Family of 4" price="49" featured features={["2 adults + 2 children", "Best value on weekends", "VR zone bookable on the day", "Cafe UFO 10% off"]} cta="Book Family Ticket" />
          <TicketCard title="Adult"       price="16" features={["Over 16", "Free re-entry on the day", "Concessions £12"]} cta="Book Adult Ticket" />
        </div>
      </section>
      <section className="mk-section" style={{paddingTop: 0}}>
        <div className="mk-panel">
          <div className="mk-split" style={{alignItems: "stretch"}}>
            <div>
              <p className="mk-eyebrow">Opening times</p>
              <h2 style={{fontFamily: "var(--ez-font-display)", fontSize: 40, textTransform: "uppercase", letterSpacing: "-0.02em", lineHeight: 0.95, color: "var(--ez-fg)", margin: "0 0 20px"}}>Seven Days a Week.</h2>
              <div className="mk-hours-card">
                <table style={{borderCollapse: "collapse", width: "100%", fontSize: 15}}>
                  <tbody>
                    {[
                      ["Monday - Friday",  "10:00 - 17:00", false],
                      ["Saturday",         "09:30 - 18:00", true],
                      ["Sunday",           "10:00 - 17:00", false],
                      ["Bank holidays",    "10:00 - 17:00", false],
                      ["Christmas Day",    "Closed",        false],
                    ].map((r, i) =>
                      <tr key={i} style={{borderBottom: i < 4 ? "1px solid var(--ez-keyline)" : "0"}}>
                        <td style={{padding: "12px 0", fontFamily: "var(--ez-font-display)", textTransform: "uppercase", letterSpacing: "0.04em", fontSize: 13, color: "var(--ez-fg)"}}>{r[0]}</td>
                        <td style={{padding: "12px 0", color: r[2] ? "var(--ez-orange)" : "var(--ez-fg)", textAlign: "right", fontWeight: r[2] ? 700 : 400}}>{r[1]}{r[2] && <span style={{marginLeft: 8, fontFamily: "var(--ez-font-display)", fontSize: 10, letterSpacing: "0.08em", color: "var(--ez-orange)"}}>BUSY</span>}</td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
              <p style={{marginTop: 20, fontSize: 14, color: "var(--ez-fg-muted)"}}>Last entry 60 minutes before close. <strong style={{color: "var(--ez-orange)"}}>Formerly Exploring Science</strong> - all old tickets still valid until 22 June 2026.</p>
            </div>
            <div className="mk-form">
              <h3>Got a Question?</h3>
              <div className="mk-field">
                <label htmlFor="t-name">Your name</label>
                <input id="t-name" type="text" placeholder="Mrs Adeyemi" />
              </div>
              <div className="mk-field">
                <label htmlFor="t-email">Email</label>
                <input id="t-email" type="email" placeholder="hello@school.uk" />
              </div>
              <div className="mk-field">
                <label htmlFor="t-msg">Your question</label>
                <textarea id="t-msg" rows="4" placeholder="Coach drop-off, group rates, anything else…" />
                <span className="mk-hint">We reply within one working day.</span>
              </div>
              <a className="mk-btn primary">Send Enquiry</a>
            </div>
          </div>
        </div>
      </section>
      <section className="mk-section" style={{paddingTop: 0}}>
        <div className="mk-callout">
          <div>
            <p style={{margin: "0 0 6px", fontFamily: "var(--ez-font-display)", fontSize: 11, letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--ez-green-on-white)"}}>Groups of 10 or more</p>
            <h3>Skip the queue. Book the whole gang in one go.</h3>
            <p>Group rates from £12 pp for 10+ bookings. We hold a coach bay, set out a meeting point, and brief your group lead. Same form, faster reply.</p>
          </div>
          <div className="mk-callout-actions">
            <a className="mk-btn primary lg">Enquire for Groups</a>
            <a className="mk-btn secondary">Schools instead</a>
          </div>
        </div>
      </section>
    </>
  );
}

// ---------------------------------------------------------
// SchoolsPage
// ---------------------------------------------------------
function SchoolsPage() {
  return (
    <>
      <section className="mk-page-hero">
        <div className="mk-page-hero-inner">
          <p className="mk-crumbs"><a href="index.html">Home</a> Schools</p>
          <h1>School Trips That Get Booked Again.</h1>
          <p>£18 per pupil, standard rate. Risk assessments, teacher prep packs, and SEND-friendly room maps included. Norfolk Short Breaks framework approved.</p>
        </div>
      </section>
      <section className="mk-section">
        <div className="mk-split">
          <div>
            <p className="mk-eyebrow">How a visit runs</p>
            <h2 style={{fontFamily: "var(--ez-font-display)", fontSize: "clamp(32px,3.5vw,44px)", textTransform: "uppercase", letterSpacing: "-0.02em", lineHeight: 0.95, color: "var(--ez-fg)", margin: "0 0 16px"}}>A Half Day or a Full Day. You Pick.</h2>
            <ul className="mk-checklist">
              <li>Free coach parking and a quiet drop-off bay on Francis Way.</li>
              <li>Pre-trip Zoom briefing for the lead teacher, 20 minutes.</li>
              <li>Floor split into six zones with a printable map per group.</li>
              <li>One staff lead per 10 pupils, free of charge.</li>
              <li>SEND-friendly floor plan and a calm room on-site.</li>
              <li>Curriculum links written for KS1, KS2, and KS3.</li>
            </ul>
            <div className="mk-quote">
              <p>"The staff briefing was the best we've ever had, and the kids still talk about the slime workshop a month later."</p>
              <cite>Mrs Adeyemi, Bowthorpe Primary &middot; KS2 visit, March 2026</cite>
            </div>
          </div>
          <div className="mk-form">
            <h3>Plan Your Visit</h3>
            <div className="mk-field">
              <label htmlFor="s-school">School name</label>
              <input id="s-school" type="text" defaultValue="Bowthorpe Primary" />
            </div>
            <div className="mk-field">
              <label htmlFor="s-ks">Key stage</label>
              <select id="s-ks" defaultValue="KS2">
                <option>KS1</option>
                <option>KS2</option>
                <option>KS3</option>
                <option>Mixed</option>
              </select>
            </div>
            <div style={{display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12}}>
              <div className="mk-field">
                <label htmlFor="s-pupils">Pupils</label>
                <input id="s-pupils" type="number" defaultValue="60" />
              </div>
              <div className="mk-field">
                <label htmlFor="s-date">Preferred date</label>
                <input id="s-date" type="date" />
              </div>
            </div>
            <div className="mk-field">
              <label htmlFor="s-send">SEND considerations</label>
              <textarea id="s-send" rows="3" placeholder="Anything our welcome team should know, e.g. a calm room slot at 11:00." />
            </div>
            <a className="mk-btn primary">Send Enquiry</a>
          </div>
        </div>
      </section>
    </>
  );
}

Object.assign(window, {
  ContinuityBar, Header, Hero, Stats, SectionHead,
  AttractionCard, Attractions, PartiesPromo, SchoolsPromo,
  Footer, PageShell, TicketCard, TicketsPage, SchoolsPage,
  BadgeStrip,
});
