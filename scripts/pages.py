#!/usr/bin/env python
# Writes the static HTML pages so the header and footer stay identical on every page.
# Run: npm run pages. Writes into site/. Edit page text here, not in the generated HTML.
import sys, os
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site')
SITE = 'https://smartstudycenters.com'   # change here if the client's domain differs
TEL = '<a href="tel:+919731045709">097310 45709</a>'
MAP = 'https://maps.google.com/?cid=1450289958892343616'
WA = 'https://wa.me/919731045709?text=Hi%2C%20I%20would%20like%20to%20know%20about%20tuition%20classes'
ic = lambda n, cls='i': f'<svg class="{cls}" aria-hidden="true"><use href="assets/icons.svg#{n}"/></svg>'
wa = '<svg aria-hidden="true"><use href="assets/icons.svg#wa"/></svg>'

def head(title, desc, path, extra='', index=True):
    canon = f'<link rel="canonical" href="{SITE}/{path}">\n' if index else ''
    robots = 'index, follow, max-image-preview:large' if index else 'noindex'
    return f'''<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#1b2a5c">
<meta name="robots" content="{robots}">
{canon}<link rel="icon" href="favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_IN">
<meta property="og:site_name" content="Smart Tutorials">
<meta property="og:url" content="{SITE}/{path}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/images/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="628">
<meta property="og:image:alt" content="The office at Smart Tutorials, Vijayanagar, Bengaluru">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="assets/fonts/Poppins-600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/site.css">
{extra}</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
'''

def header(home):
    p = '' if home else './'
    nav = [('home','Home'),('about','About Us'),('courses','Courses'),('gallery','Gallery'),('reviews','Reviews'),('faq','FAQs'),('contact','Contact')]
    active = ' class="active"'
    main_links = '\n      '.join(f'<a href="{p}#{a}"{active if home and a=="home" else ""}>{t}</a>' for a,t in nav)
    m_links = '\n    '.join(f'<a href="{p}#{a}">{t}</a>' for a,t in nav)
    return f'''
<div class="topbar">
  <div class="container">
    <div class="left">
      <a href="tel:+919731045709">{ic('phone')}097310 45709</a>
      <span class="hide-m">{ic('clock')}10:00 AM – 10:00 PM</span>
      <span class="hide-m">{ic('pin')}Vijayanagar II Stage, Bengaluru</span>
    </div>
    <div class="social">
      <a href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp (opens in a new tab)">{wa}</a>
    </div>
  </div>
</div>

<header id="hdr">
  <div class="container">
    <a href="{p}#home" class="logo">
      <span class="mark" aria-hidden="true">ST</span>
      <span><span class="name">SMART <span>TUTORIALS</span></span><small>Today a reader, Tomorrow a Leader</small></span>
    </a>
    <nav class="main" aria-label="Main">
      {main_links}
      <a href="{p}#enquiry" class="btn btn-red">Enquire Now</a>
    </nav>
    <button class="burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="mnav">{ic('menu')}</button>
  </div>
  <div class="m-nav" id="mnav">
    {m_links}
    <a href="tel:+919731045709" class="btn btn-yellow">Call 097310 45709</a>
  </div>
</header>
'''

def footer(home):
    p = '' if home else './'
    return f'''
<footer>
  <div class="container">
    <div class="f-cta">
      <div><h3>Admissions are open. Book your free demo class.</h3><p>Visit us at Vijayanagar II Stage or call to know about batch timings.</p></div>
      <a href="tel:+919731045709">{ic('phone')}&nbsp; 097310 45709</a>
    </div>
  </div>
  <div class="container f-top">
    <div class="about-f">
      <a href="{p}#home" class="logo"><span class="mark" aria-hidden="true">ST</span><span><span class="name">SMART <span>TUTORIALS</span></span><small>Vijayanagar, Bengaluru</small></span></a>
      <p>A unit of Smart Study Center, helping students of Class 8, 9, 10 and PUC learn with clarity and confidence. Today a reader, Tomorrow a Leader.</p>
      <div class="f-social">
        <a href="tel:+919731045709" aria-label="Call Smart Tutorials">{ic('phone')}</a>
        <a href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp (opens in a new tab)">{wa}</a>
        <a href="{MAP}" target="_blank" rel="noopener" aria-label="Google Maps (opens in a new tab)">{ic('pin')}</a>
      </div>
    </div>
    <div>
      <h4>Courses</h4>
      <ul>
        <li><a href="class-8-9-tuition-vijayanagar.html">Class 8 &amp; 9 Tuition</a></li>
        <li><a href="class-10-tuition-vijayanagar.html">Class 10 Tuition</a></li>
        <li><a href="puc-tuition-vijayanagar.html">PUC Tuition</a></li>
        <li><a href="{p}#reviews">Reviews</a></li>
        <li><a href="{p}#contact">Contact Us</a></li>
      </ul>
    </div>
    <div>
      <h4>Information</h4>
      <ul>
        <li><a href="disclosures.html">Disclosures &amp; Helplines</a></li>
        <li><a href="privacy.html">Privacy Notice</a></li>
        <li><a href="terms.html">Terms of Use</a></li>
      </ul>
    </div>
    <div>
      <h4>Get in Touch</h4>
      <ul class="ci">
        <li>{ic('pin')}<span>822, 9th Main Road, near Brooklyn National Public School, Vijaya Nagar II Stage, Bengaluru – 560104</span></li>
        <li>{ic('phone')}<a href="tel:+919731045709">097310 45709</a></li>
        <li>{ic('clock')}<span>10:00 AM – 10:00 PM</span></li>
      </ul>
    </div>
  </div>
  <div class="f-notice">
    <div class="container">Joining any tuition programme does not guarantee marks, ranks or admission. Results depend on each student's effort and circumstances. <a href="disclosures.html">Read our disclosures</a>.</div>
  </div>
  <div class="f-bottom">
    <div class="container">
      <span>© <span id="yr">2026</span> Smart Tutorials. All Rights Reserved.</span>
      <span>Designed &amp; Developed by <span class="credit">Ramify Technologies</span></span>
    </div>
  </div>
</footer>

<div class="float-btns">
  <a href="#main" class="to-top" id="toTop" aria-label="Back to top">{ic('up')}</a>
  <a href="tel:+919731045709" class="call" aria-label="Call">{ic('phone')}</a>
  <a href="{WA}" class="wa" target="_blank" rel="noopener" aria-label="WhatsApp (opens in a new tab)">{wa}</a>
</div>

<nav class="m-bar" aria-label="Quick contact">
  <a href="tel:+919731045709">{ic('phone')}Call</a>
  <a href="{WA}" class="wa-b" target="_blank" rel="noopener">{wa}WhatsApp</a>
  <a href="{p}#enquiry" class="enq-b">Enquire Now</a>
</nav>

<script src="assets/site.js" defer></script>
</body>
</html>
'''

def slide(cls, img, alt, tag, htag, h, body, btns, eager=False, trust=''):
    a = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'''
    <div class="slide{' active' if eager else ''}">
      <div class="art has-photo"><img src="images/centre/{img}.webp" srcset="images/centre/{img}-960.webp 960w, images/centre/{img}.webp 1920w" sizes="(max-width:768px) 640px, 100vw" alt="{alt}" width="1920" height="814" {a}></div>
      <div class="container cap">
        <span class="tag">{tag}</span>
        <{htag}>{h}</{htag}>
        {body}
        <div class="btns">{btns}</div>{trust}
      </div>
    </div>'''

def course(title, range_, meta, desc, items, icon, extra='', ribbon='', url=''):
    lis = ''.join(f'<li>{ic("right")}{x}</li>' for x in items)
    metas = ''.join(f'<em>{m}</em>' for m in meta)
    return f'''
      <div class="course fade-in{extra}">
        {ribbon}
        <div class="head"><div><span class="h-ico">{ic(icon)}</span><h3>{title}</h3></div><span>{range_}</span></div>
        <div class="body">
          <div class="meta">{metas}</div>
          <p>{desc}</p>
          <ul>{lis}</ul>
          <div class="links"><a href="{url}">{title} tuition details →</a><a href="#enquiry">Book a free demo</a></div>
        </div>
      </div>'''

faqs = [
 ('What are the centre timings?', 'The centre is open from 10:00 AM to 10:00 PM. Please call to confirm the batch timing for your class, as batches are planned around school and college hours.'),
 ('Which classes and boards do you teach?', 'We teach Class 8, 9, 10 and PUC students, and cover ICSE, CBSE and State syllabus.'),
 ('Where is Smart Tutorials located?', '822, 9th Main Road, near Brooklyn National Public School, Vijaya Nagar II Stage, Hampi Nagar, RPC Layout, Bengaluru – 560104.'),
 ('Do you offer one-to-one classes?', 'Yes. Along with regular batches, one-to-one sessions are available for students who need extra attention in a subject. Call us to check availability.'),
 ('Can my child attend a demo class first?', 'Yes, a free demo class is available. Call us or fill the enquiry form and we will fix a convenient time.'),
 ('What are the fees?', f'Fees depend on the class, board and subjects. Please call {TEL} or visit the centre for the current fee details and refund terms, in writing, before you decide.'),
 ('Do you guarantee marks or ranks?', 'No. We do not guarantee marks, ranks or admission anywhere. We focus on clear teaching, regular practice and doubt clearing. Results depend on each student.'),
 ('How do I track my child\'s progress?', 'Students take regular tests, and parents can speak with the teachers about how their child is doing.'),
]

def index():
    import json, re
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', a)}} for q, a in faqs]}, ensure_ascii=False)
    ld = f'''<script type="application/ld+json">
{{"@context":"https://schema.org","@type":["EducationalOrganization","LocalBusiness"],"@id":"{SITE}/#org","name":"Smart Tutorials","description":"Tuition for Class 8, 9, 10 and PUC students, covering ICSE, CBSE and State syllabus.","sameAs":["{MAP}"],"alternateName":"Smart Tutorials, a unit of Smart Study Center","url":"{SITE}/","telephone":"+91-97310-45709","image":"{SITE}/images/og-image.jpg","slogan":"Today a reader, Tomorrow a Leader","address":{{"@type":"PostalAddress","streetAddress":"822, 9th Main Road, near Brooklyn National Public School, Vijaya Nagar II Stage, Hampi Nagar, RPC Layout","addressLocality":"Bengaluru","addressRegion":"Karnataka","postalCode":"560104","addressCountry":"IN"}},"geo":{{"@type":"GeoCoordinates","latitude":12.9584351,"longitude":77.5365863}},"hasMap":"{MAP}","areaServed":["Vijayanagar","Hampi Nagar","RPC Layout","Bengaluru"]}}
</script>
<script type="application/ld+json">
{faq_ld}
</script>
<link rel="preload" as="image" href="images/centre/banner-office.webp" imagesrcset="images/centre/banner-office-960.webp 960w, images/centre/banner-office.webp 1920w" imagesizes="(max-width:768px) 640px, 100vw" fetchpriority="high">
'''
    s = head('Class 8–10 &amp; PUC Tuition in Vijayanagar | Smart Tutorials',
             'Tuition for Class 8, 9, 10 and PUC (ICSE, CBSE, State) in Vijayanagar II Stage, Bengaluru. One-to-one sessions and a free demo class. Call 097310 45709.', '', ld)
    s += header(True)
    s += f'''
<div class="ticker" role="region" aria-label="Notice">
  <b>Notice</b>
  <div class="run-wrap"><div class="run">Admissions open for Class 8, 9, 10 &amp; PUC &nbsp;•&nbsp; ICSE, CBSE &amp; State &nbsp;•&nbsp; Free demo class available &nbsp;•&nbsp; One-to-one sessions for students who need extra attention &nbsp;•&nbsp; Call 097310 45709 to book a visit</div></div>
</div>

<main id="main">
<section class="slider" id="home" aria-roledescription="carousel" aria-label="Smart Tutorials highlights">
  <div class="slides" id="slides">'''
    s += slide('s1','banner-office','At work in the Smart Tutorials office','Admissions Open','h1','Tuition Classes in <span>Vijayanagar</span>, Bengaluru',
        '<p>Class 8, 9, 10 &amp; PUC · ICSE, CBSE &amp; State · Experienced teachers in a friendly, homely atmosphere.</p>',
        '<a href="#enquiry" class="btn btn-yellow">Book Free Demo</a><a href="tel:+919731045709" class="btn btn-outline">Call 097310 45709</a>', True,
        '<div class="trust"><span class="stars" aria-hidden="true"><i>★★★★★</i></span><span><b>4.7</b> on Google · 157 reviews, as on 4 Nov 2026</span></div>')
    s += slide('s2','banner-tests','Students writing a test at Smart Tutorials, faces blurred for privacy','Rated 4.7 on Google','h2','Loved by Parents.<br><span>Trusted by Students.</span>',
        '<blockquote>"Teaching quality and quantity is very satisfying." <small>A review on Google</small></blockquote>',
        '<a href="#reviews" class="btn btn-yellow">Read Reviews</a><a href="#enquiry" class="btn btn-outline">Enquire Now</a>')
    s += slide('s3','banner-classroom','A classroom with wooden benches at Smart Tutorials','One-to-One Sessions','h2','Personal Attention for <span>Every Student</span>',
        '<p>Extra help in a subject, at a pace that suits your child. Doubts are cleared patiently.</p>',
        '<a href="#enquiry" class="btn btn-yellow">Book a Session</a><a href="#courses" class="btn btn-outline">View Courses</a>', False,
        f'<ul class="trust chips"><li>{ic("check")}Free demo class</li><li>{ic("check")}ICSE · CBSE · State</li></ul>')
    s += f'''
  </div>
  <button class="sl-arrow prev" id="slPrev" type="button" aria-label="Previous slide">{ic('right')}</button>
  <button class="sl-arrow next" id="slNext" type="button" aria-label="Next slide">{ic('right')}</button>
  <a class="hero-card" href="#contact"><span class="hc-ico">{ic('pin')}</span><span><b>Visit us on 9th Main Road</b><small>Vijayanagar II Stage · 10 AM – 10 PM</small></span></a>
</section>

<section class="features" aria-label="Highlights">
  <div class="container">
    <div class="feat fade-in"><span class="ico">{ic('star')}</span><div><p class="feat-t">4.7 on Google</p><p>From 157 reviews, as on 4 Nov 2026</p></div></div>
    <div class="feat fade-in"><span class="ico">{ic('teacher')}</span><div><p class="feat-t">Experienced Teachers</p><p>Approachable and dedicated</p></div></div>
    <div class="feat fade-in"><span class="ico">{ic('users')}</span><div><p class="feat-t">One-to-One Sessions</p><p>Personal attention when needed</p></div></div>
    <div class="feat fade-in"><span class="ico">{ic('clock')}</span><div><p class="feat-t">10 AM – 10 PM</p><p>Centre timings</p></div></div>
  </div>
</section>

<section class="about" id="about">
  <div class="container">
    <div class="photo">
      <div class="img"><img src="images/centre/building.webp" srcset="images/centre/building-480.webp 480w, images/centre/building.webp 706w" sizes="(max-width:992px) 90vw, 540px" alt="The Smart Tutorials building on 9th Main Road, Vijayanagar, with its red name board" width="706" height="377" loading="lazy"></div>
      <div class="badge"><b>4.7</b><span>Google Rating</span></div>
    </div>
    <div>
      <p class="eyebrow">About Us</p>
      <h2>A tuition centre for students in Vijayanagar</h2>
      <p>Smart Tutorials, a unit of Smart Study Center, is on 9th Main Road, Vijayanagar II Stage, near Brooklyn National Public School. We teach Class 8, 9, 10 and PUC students from ICSE, CBSE and State syllabus, in the Hampi Nagar and RPC Layout area of Vijayanagar.</p>
      <p class="vision">We want every student to walk out of our classes sure of what they have learned, responsible for their own work and ready to do their very best.</p>
      <blockquote>"Teachers are approachable and homely atmosphere and best place for students." <small>A review on Google</small></blockquote>
      <ul class="checks">
        <li>{ic('check')}Clear concept teaching</li>
        <li>{ic('check')}Patient doubt solving</li>
        <li>{ic('check')}Regular tests</li>
        <li>{ic('check')}LGBTQ+ friendly space</li>
      </ul>
      <a href="#contact" class="btn btn-red">Visit Our Centre</a>
    </div>
  </div>
</section>

<section id="courses">
  <div class="container">
    <div class="sec-title">
      <h2>Our <span>Courses</span></h2>
      <p>Class 8, 9, 10 and PUC tuition in Vijayanagar, Bengaluru, with batch and one-to-one options.</p>
    </div>
    <div class="courses-grid">'''
    s += course('Class 8 &amp; 9','High School',['ICSE','CBSE','State'],'Strong understanding in every core subject before the board year.',['Maths &amp; Science','Social Science','English &amp; languages'],'book',url='class-8-9-tuition-vijayanagar.html')
    s += course('Class 10','SSLC',['ICSE','CBSE','State'],'Special coaching for the board year, with regular tests and revision.',['Maths, Physics, Chemistry, Biology','Social Science &amp; languages','Board exam preparation'],'star',' popular','<span class="ribbon">Special</span>',url='class-10-tuition-vijayanagar.html')
    s += course('PUC','I &amp; II PUC',['Karnataka PUC'],'Coaching for pre-university students. Call us to check the subjects and batches running now.',['Subject-wise coaching','Regular tests','Doubt clearing'],'users',url='puc-tuition-vijayanagar.html')
    s += f'''
    </div>
    <div class="boards"><span>ICSE</span><span>CBSE</span><span>State Board</span><span>One-to-One Classes</span></div>
    <p class="assure">We do not guarantee marks, ranks or admission. Your child's results depend on their own effort. See our <a href="disclosures.html">disclosures</a> for details on teachers, fees and refunds.</p>
  </div>
</section>

<section class="hero" id="demo">
  <div class="container">
    <div>
      <span class="tag">Free Demo Class</span>
      <h2 class="h-big">Not sure yet? <span>Try a class for free.</span></h2>
      <p>See how we teach before you decide. Meet the teachers, sit in a class and ask your questions in a friendly, homely atmosphere.</p>
      <ul>
        <li>{ic('check')}Experienced teachers</li>
        <li>{ic('check')}One-to-one sessions</li>
        <li>{ic('check')}Regular tests &amp; doubt clearing</li>
        <li>{ic('check')}Open till 10 PM</li>
      </ul>
      <div class="btns">
        <a href="tel:+919731045709" class="btn btn-yellow">{ic('phone')} Call Now</a>
        <a href="#courses" class="btn btn-outline">View Courses</a>
      </div>
      <div class="rating-line"><span class="g">Google</span><span><b>4.7</b> out of 5 · 157 reviews, as on 4 Nov 2026</span></div>
    </div>

    <div class="enquiry" id="enquiry">
      <h3>Book a Free Demo Class<small>Send your details to us on WhatsApp</small></h3>
      <form id="enqForm" novalidate>
        <div>
          <label for="fName">Parent / guardian name <span class="req" aria-hidden="true">*</span></label>
          <input id="fName" autocomplete="name" required aria-describedby="fNameErr">
          <p class="field-err" id="fNameErr">Please enter your name.</p>
        </div>
        <div>
          <label for="fPhone">Mobile number <span class="req" aria-hidden="true">*</span></label>
          <input id="fPhone" type="tel" inputmode="tel" maxlength="16" autocomplete="tel" required aria-describedby="fPhoneErr">
          <p class="field-err" id="fPhoneErr">Please enter a valid 10-digit mobile number.</p>
        </div>
        <div class="two">
          <div>
            <label for="fClass">Class</label>
            <select id="fClass"><option value="">Select</option><option>Class 8</option><option>Class 9</option><option>Class 10</option><option>I PUC</option><option>II PUC</option></select>
          </div>
          <div>
            <label for="fBoard">Board</label>
            <select id="fBoard"><option value="">Select</option><option>ICSE</option><option>CBSE</option><option>State</option><option>Karnataka PUC</option></select>
          </div>
        </div>
        <div>
          <label for="fMsg">Message (optional)</label>
          <textarea id="fMsg" rows="2"></textarea>
        </div>
        <div>
          <label class="check"><input id="fConsent" type="checkbox" required aria-describedby="fConsentErr"><span>I am the student's parent or guardian, or I am 18 or older, and I agree to Smart Tutorials contacting me about this enquiry. Read the <a href="privacy.html">Privacy Notice</a>.</span></label>
          <p class="field-err" id="fConsentErr">Please tick this box to continue.</p>
        </div>
        <button class="btn btn-wa" type="submit">{wa}Continue on WhatsApp</button>
        <p class="note">This website does not store your details. They reach us only when you press send in WhatsApp. Or call <a href="tel:+919731045709"><b>097310 45709</b></a>.</p>
      </form>
      <div class="form-ok" id="formOk" tabindex="-1" role="status">
        <h4>Almost done</h4>
        <p>Your message is ready in WhatsApp. Press send there, and your enquiry reaches us.</p>
        <a id="waSend" class="btn btn-wa" target="_blank" rel="noopener" href="https://wa.me/919731045709">{wa}Open WhatsApp</a>
        <p class="alt">No WhatsApp? Call <a href="tel:+919731045709">097310 45709</a>.</p>
      </div>
    </div>
  </div>
</section>

<section class="subjects">
  <div class="container">
    <div class="sec-title"><h2>Subjects We <span>Teach</span></h2></div>
    <div class="sub-grid">
      <div class="sub fade-in"><div class="ico c1" aria-hidden="true">∑</div><h3 class="h4">Mathematics</h3><small>All classes</small></div>
      <div class="sub fade-in"><div class="ico c2" aria-hidden="true">{ic('star')}</div><h3 class="h4">Science</h3><small>Phy · Chem · Bio</small></div>
      <div class="sub fade-in"><div class="ico c3" aria-hidden="true">Aa</div><h3 class="h4">English</h3><small>Grammar &amp; writing</small></div>
      <div class="sub fade-in"><div class="ico c4" aria-hidden="true">ಕ</div><h3 class="h4">Languages</h3><small>Kannada · Sanskrit</small></div>
      <div class="sub fade-in"><div class="ico c5" aria-hidden="true">{ic('globe')}</div><h3 class="h4">Social Science</h3><small>Hist · Geo · Civics</small></div>
      <div class="sub fade-in"><div class="ico c6" aria-hidden="true">{ic('book')}</div><h3 class="h4">Computer Applications</h3><small>As per syllabus</small></div>
    </div>
  </div>
</section>

<section class="why">
  <div class="container">
    <div class="sec-title">
      <h2>Why Choose Smart Tutorials?</h2>
      <p>What students and parents mention in their Google reviews.</p>
    </div>
    <div class="why-grid">
      <div class="why-item fade-in"><span class="n">01</span><h3>Experienced Teachers</h3><p>Teachers who know the syllabus well and explain it in simple language.</p></div>
      <div class="why-item fade-in"><span class="n">02</span><h3>Individual Care</h3><p>One-to-one sessions for students who need extra help in a subject.</p></div>
      <div class="why-item fade-in"><span class="n">03</span><h3>Doubt Clearing</h3><p>Students are encouraged to ask questions until the topic is clear.</p></div>
      <div class="why-item fade-in"><span class="n">04</span><h3>Homely Atmosphere</h3><p>A friendly place where students feel comfortable and focused.</p></div>
      <div class="why-item fade-in"><span class="n">05</span><h3>Weekly Tests</h3><p>Regular practice that shows students where they stand.</p></div>
      <div class="why-item fade-in"><span class="n">06</span><h3>Disciplined Classes</h3><p>A steady routine that helps students stay on top of their work.</p></div>
    </div>
  </div>
</section>

<section class="process">
  <div class="container">
    <div class="sec-title">
      <h2>How to <span>Join</span></h2>
      <p>Getting started at Smart Tutorials is simple.</p>
    </div>
    <div class="steps">
      <div class="step fade-in"><div class="circle"><b>1</b>{ic('phone')}</div><div><h3 class="h4">Call or Enquire</h3><p>Call us or fill the enquiry form with your child's class and board.</p></div></div>
      <div class="step fade-in"><div class="circle"><b>2</b>{ic('pin')}</div><div><h3 class="h4">Visit the Centre</h3><p>Come to 9th Main Road, Vijayanagar and meet our teachers.</p></div></div>
      <div class="step fade-in"><div class="circle"><b>3</b>{ic('book')}</div><div><h3 class="h4">Attend a Free Demo</h3><p>Your child sits in a class to see how we teach.</p></div></div>
      <div class="step fade-in"><div class="circle"><b>4</b>{ic('check')}</div><div><h3 class="h4">Join the Batch</h3><p>Pick a batch or one-to-one timing that fits school or college hours.</p></div></div>
    </div>
  </div>
</section>

<section class="gallery" id="gallery">
  <div class="container">
    <div class="sec-title">
      <h2>Inside Our <span>Centre</span></h2>
      <p>Real photos from Smart Tutorials. Students' faces are blurred to protect their privacy.</p>
    </div>
    <div class="gal-grid">
      <figure class="fade-in"><img src="images/centre/classroom.webp" srcset="images/centre/classroom-480.webp 480w, images/centre/classroom.webp 960w" sizes="(max-width:992px) 50vw, 360px" width="960" height="720" loading="lazy" alt="Rows of wooden benches in a Smart Tutorials classroom"><figcaption>Classroom</figcaption></figure>
      <figure class="fade-in"><img src="images/centre/tests.webp" srcset="images/centre/tests-480.webp 480w, images/centre/tests.webp 960w" sizes="(max-width:992px) 50vw, 360px" width="960" height="540" loading="lazy" alt="Students writing a test at wooden desks, faces blurred"><figcaption>Regular tests</figcaption></figure>
      <figure class="fade-in"><img src="images/centre/office.webp" srcset="images/centre/office-480.webp 480w, images/centre/office.webp 960w" sizes="(max-width:992px) 50vw, 360px" width="960" height="720" loading="lazy" alt="A staff member working at a desk in the Smart Tutorials office"><figcaption>Our office</figcaption></figure>
      <figure class="fade-in"><img src="images/centre/building.webp" srcset="images/centre/building-480.webp 480w, images/centre/building.webp 706w" sizes="(max-width:992px) 50vw, 360px" width="706" height="377" loading="lazy" alt="The Smart Tutorials building with its red name board"><figcaption>Our building on 9th Main Road</figcaption></figure>
      <figure class="fade-in"><img src="images/centre/lamp.webp" srcset="images/centre/lamp-480.webp 480w, images/centre/lamp.webp 720w" sizes="(max-width:992px) 50vw, 360px" width="720" height="540" loading="lazy" alt="A brass lamp decorated with yellow marigolds at a centre function"><figcaption>Lamp lighting at a function</figcaption></figure>
      <figure class="fade-in"><img src="images/centre/rangoli.webp" srcset="images/centre/rangoli-480.webp 480w, images/centre/rangoli.webp 544w" sizes="(max-width:992px) 50vw, 360px" width="544" height="408" loading="lazy" alt="A flower arrangement of yellow and white blooms in a clay bowl"><figcaption>Celebrations at the centre</figcaption></figure>
    </div>
  </div>
</section>

<section class="reviews" id="reviews">
  <div class="container">
    <div class="sec-title"><h2>What <span>Students &amp; Parents</span> Say</h2></div>
    <div class="g-summary">
      <span class="gword">Google</span>
      <span class="score">4.7</span>
      <span>out of 5<small>157 reviews, as on 4 Nov 2026</small></span>
    </div>
    <div class="rev-grid">
      <div class="rev fade-in"><p>"My tuition classes are quite helpful and well-structured. The teacher explains concepts in a clear and simple way, making even difficult topics easier to understand. Doubts are usually solved patiently."</p><div class="src">A student's review on Google</div></div>
      <div class="rev fade-in"><p>"Teaching quality and quantity is very satisfying. Good place for children to grow."</p><div class="src">A review on Google</div></div>
      <div class="rev fade-in"><p>"He has been managing his work better and gets his queries addressed."</p><div class="src">A review on Google</div></div>
    </div>
    <p class="swipe-hint">Swipe to read more →</p>
    <p class="rev-note">These are selected excerpts, and reviewers' names are left out for privacy. Experiences differ from student to student. Please read all the reviews on Google, including the critical ones, before you decide.</p>
    <div class="center"><a class="btn btn-navy" href="{MAP}" target="_blank" rel="noopener">See all reviews on Google</a></div>
  </div>
</section>

<section class="faq" id="faq">
  <div class="container">
    <div>
      <div class="sec-title"><h2>Frequently Asked <span>Questions</span></h2></div>
      <p>Common questions parents ask before joining.</p>
      <div class="help">
        <h3 class="h4">Still have a question?</h3>
        <p>Talk to us directly. We're happy to help.</p>
        <a href="tel:+919731045709" class="btn btn-yellow">Call 097310 45709</a>
      </div>
    </div>
    <div>
      {''.join(f'<details{" open" if i==0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i,(q,a) in enumerate(faqs))}
    </div>
  </div>
</section>

<div class="cta">
  <div class="container">
    <div>
      <h2>Looking for tuition near Vijayanagar?</h2>
      <p>Visit the centre, meet the teachers and attend a free demo class.</p>
    </div>
    <div class="btns">
      <a href="tel:+919731045709" class="btn btn-navy">Call 097310 45709</a>
      <a href="#enquiry" class="btn btn-line">Book Free Demo</a>
    </div>
  </div>
</div>

<section class="contact" id="contact">
  <div class="container">
    <div>
      <div class="sec-title sec-left"><h2>Contact <span>Us</span></h2></div>
      <div class="c-list">
        <div class="c-item"><span class="ico">{ic('pin')}</span><div><h3 class="h4">Address</h3><p>822, 9th Main Road, near Brooklyn National Public School, Vijaya Nagar II Stage, Hampi Nagar, RPC Layout, Bengaluru, Karnataka 560104</p></div></div>
        <div class="c-item"><span class="ico">{ic('phone')}</span><div><h3 class="h4">Phone &amp; WhatsApp</h3><a href="tel:+919731045709">097310 45709</a></div></div>
        <div class="c-item"><span class="ico">{ic('clock')}</span><div><h3 class="h4">Timings</h3><p>10:00 AM – 10:00 PM</p></div></div>
      </div>
    </div>
    <div class="map" id="mapBox">
      <div class="map-load">
        {ic('pin')}
        <h3>Find us on the map</h3>
        <p>The map comes from Google. Google may set cookies and see your IP address once you load it.</p>
        <div class="btns">
          <button class="btn btn-navy" id="mapLoad" type="button" data-src="https://maps.google.com/maps?q=SMART%20TUTORIALS%2C%20822%209th%20Main%20Road%2C%20Vijaya%20Nagar%20II%20Stage%2C%20Bengaluru%20560104&amp;z=16&amp;output=embed">Load map here</button>
          <a class="btn btn-red" href="{MAP}" target="_blank" rel="noopener">Open in Google Maps</a>
        </div>
      </div>
    </div>
  </div>
</section>
</main>
'''
    s += footer(True)
    return s

def page(path, title, desc, h1, sub, body):
    import json, html as _h
    crumbs = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": _h.unescape(title), "item": f"{SITE}/{path}"}]})
    ld = f'<script type="application/ld+json">{crumbs}</script>\n'
    return head(f'{title} | Smart Tutorials', desc, path, ld) + header(False) + f'''
<main id="main">
<div class="page-head"><div class="container"><h1>{h1}</h1><p>{sub}</p></div></div>
<div class="prose"><div class="container">
{body}
</div></div>
</main>
''' + footer(False)

privacy = page('privacy.html','Privacy Notice','How Smart Tutorials handles personal data shared through this website.','Privacy Notice','Last updated: 4 November 2026', f'''
<h2>Who we are</h2>
<p>Smart Tutorials, a unit of Smart Study Center, 822, 9th Main Road, Vijaya Nagar II Stage, Bengaluru 560104, decides how personal data shared with us for enquiries is used. This notice follows India's Digital Personal Data Protection Act, 2023 and the rules made under it.</p>
<h2>What this website collects</h2>
<p>This website has no user accounts and does not save enquiry form details on any server. The form prepares a WhatsApp message on your own device. We receive the details only if you press send in WhatsApp.</p>
<div class="tbl"><table>
<tr><th scope="col">What we receive</th><th scope="col">Why</th></tr>
<tr><td>Parent or guardian name and mobile number</td><td>To reply to your enquiry and arrange a demo class</td></tr>
<tr><td>Student's class and board, if you share them</td><td>To suggest the right batch</td></tr>
<tr><td>Anything you write in your message</td><td>To answer your question</td></tr>
</table></div>
<p>Please do not share sensitive details about a student's health or family in your message.</p>
<h2>Children's data</h2>
<p>Enquiries should come from a parent or guardian, or from a person aged 18 or older. We do not use this website to track children's behaviour or to show them targeted advertising. Students' faces in our website photos are blurred, and we do not publish a student's name, photo or result without written consent.</p>
<h2>Cookies and tracking</h2>
<p>This website does not set cookies and does not use analytics or advertising trackers. If this changes, we will update this notice and ask for your consent where needed.</p>
<h2>Other services</h2>
<ul>
<li><b>WhatsApp:</b> messages you send are also handled under WhatsApp's own privacy terms.</li>
<li><b>Google Maps:</b> the map loads only if you choose to load it. Google may then set cookies and receive your IP address. Links to Google Maps and Google reviews take you to Google's site.</li>
<li><b>Website hosting:</b> our hosting provider may keep short-term technical logs, such as IP addresses, for security and to keep the site running.</li>
</ul>
<h2>Who sees your data and how long we keep it</h2>
<p>Only staff who handle enquiries see your details. We do not sell them. We keep enquiry messages only as long as needed to respond and to run any admission that follows, unless the law requires us to keep them longer.</p>
<h2>Your rights</h2>
<p>You may ask us for a summary of your data, ask us to correct or erase it, withdraw your consent, raise a grievance, or nominate someone to act for you. Withdrawing consent is as easy as asking us; we will then stop using your details for this enquiry.</p>
<h2>Contact and complaints</h2>
<p>Call {TEL} or write to us at the address above, marked "Privacy". If you are not satisfied with our reply, you may complain to the Data Protection Board of India.</p>
''')

terms = page('terms.html','Terms of Use','Terms for using the Smart Tutorials website, including fees, refunds and our no-guarantee statement on results.','Terms of Use','Last updated: 4 November 2026', f'''
<h2>Using this website</h2>
<p>This website gives general information about Smart Tutorials. By using it, you agree to these terms. Please confirm batch timings, subjects and fees with the centre before you make a decision.</p>
<h2>No guarantee of results</h2>
<p>Enrolling at Smart Tutorials does not guarantee any marks, rank, admission or other result. Results depend on each student's effort and circumstances.</p>
<h2>Fees and refunds</h2>
<p>Admission, fees and refunds are governed by the written terms the centre gives you before admission. This website does not take payments. Please ask for the terms in writing before you pay.</p>
<h2>Reviews and third-party links</h2>
<p>Review excerpts on this website were written by users on Google and reflect their own experience. Links to WhatsApp and Google take you to services we do not control.</p>
<h2>Content</h2>
<p>The text and photos on this website belong to Smart Tutorials or are used with permission. Please ask us before reusing them. If a photo of you or your child appears here and you want it removed, call {TEL} and we will act on your request.</p>
<h2>Governing law</h2>
<p>These terms are governed by the laws of India, and courts in Bengaluru have jurisdiction. This does not affect your rights under the Consumer Protection Act, 2019.</p>
<h2>Contact</h2>
<p>Smart Tutorials, 822, 9th Main Road, Vijaya Nagar II Stage, Bengaluru 560104. Phone: {TEL}.</p>
''')

disclosures = page('disclosures.html','Disclosures &amp; Helplines','Courses, teacher qualifications, fees, results, complaint process and student helplines at Smart Tutorials.','Disclosures &amp; Helplines','Clear information for parents and students. Last updated: 4 November 2026', f'''
<h2>About the centre</h2>
<p>Smart Tutorials is a unit of Smart Study Center (Reg.), at 822, 9th Main Road, Vijaya Nagar II Stage, Bengaluru 560104. Please ask at the office to see registration documents.</p>
<h2>Courses</h2>
<div class="tbl"><table>
<tr><th scope="col">Course</th><th scope="col">Syllabus</th><th scope="col">Mode</th></tr>
<tr><td>Class 8 &amp; 9</td><td>ICSE, CBSE, State</td><td>Classroom batches, one-to-one on request</td></tr>
<tr><td>Class 10</td><td>ICSE, CBSE, State (SSLC)</td><td>Classroom batches, one-to-one on request</td></tr>
<tr><td>I &amp; II PUC</td><td>Karnataka PUC</td><td>Please call for current subjects and batches</td></tr>
</table></div>
<p>Our courses are private coaching. They are not a school programme and do not lead to a certificate or degree from a recognised board or university.</p>
<h2>Teachers' qualifications</h2>
<p>As listed on the faculty board at our centre:</p>
<ul>
<li>Maths and Science: M.Sc., B.Ed.</li>
<li>English, Social Science and Sanskrit: M.A., B.Ed.</li>
<li>Computer Applications: M.Sc. (Computer Science)</li>
</ul>
<p>Ask at the centre for the current list of teachers and subjects.</p>
<h2>Fees and refunds</h2>
<p>Fees depend on the class, board and subjects. Please call {TEL} for the current fee and ask for the fee and refund terms in writing before you pay.</p>
<h2>Results and reviews</h2>
<p><b>We do not guarantee marks, ranks or admission.</b> Joining any tuition programme does not assure success in an examination.</p>
<p>Our Google rating of 4.7 is from 157 reviews, as on 4 November 2026, and it changes over time. You can <a href="{MAP}" target="_blank" rel="noopener">read all the reviews on Google</a>. We use a student's name, photo or result in advertising only with written consent.</p>
<h2>Complaints</h2>
<p>Please tell us first. Call {TEL} or write to the centre's office, and we will try to resolve your concern quickly. You may also contact the National Consumer Helpline on <a href="tel:1915">1915</a>.</p>
<h2>Student safety and support helplines</h2>
<div class="tbl"><table>
<tr><th scope="col">Service</th><th scope="col">Number</th></tr>
<tr><td>Emergency response (police, fire, ambulance)</td><td><a href="tel:112">112</a></td></tr>
<tr><td>Tele-MANAS, free mental health support, 24 hours</td><td><a href="tel:14416">14416</a></td></tr>
<tr><td>Childline, for children in need of help</td><td><a href="tel:1098">1098</a></td></tr>
<tr><td>Women's helpline</td><td><a href="tel:181">181</a></td></tr>
<tr><td>National anti-ragging helpline</td><td><a href="tel:18001805522">1800-180-5522</a></td></tr>
</table></div>
<p>If a student feels overwhelmed by studies or exams, please talk to a parent, a teacher or one of these services. Asking for help is always the right thing to do.</p>
''')

nf = head('Page Not Found | Smart Tutorials','This page could not be found on the Smart Tutorials website. Go to the home page or call us.','404.html','',False) + header(False) + f'''
<main id="main"><div class="notfound"><div class="container">
<h1>Page not found</h1>
<p>The page you are looking for is not here.</p>
<div class="btns"><a class="btn btn-red" href="./">Go to home page</a><a class="btn btn-navy" href="tel:+919731045709">Call 097310 45709</a></div>
</div></div></main>
''' + footer(False)


def course_page(path, short, title, desc, h1, sub, img, img_w, img_h, alt, cap, body, cfaqs, related):
    import json, re
    url = f'{SITE}/{path}'
    plain = lambda t: re.sub(r'<[^>]+>', '', t).replace('&amp;', '&')
    data = [
        {"@context": "https://schema.org", "@type": "Course", "name": plain(h1), "description": desc, "url": url,
         "provider": {"@type": "EducationalOrganization", "@id": f"{SITE}/#org", "name": "Smart Tutorials", "url": f"{SITE}/"},
         "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "Onsite",
                               "location": {"@type": "Place", "name": "Smart Tutorials", "address": "822, 9th Main Road, Vijaya Nagar II Stage, Bengaluru 560104"}}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": plain(short), "item": url}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in cfaqs]},
    ]
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>\n' for d in data)
    faq_html = ''.join(f'<h3>{q}</h3><p>{a}</p>' for q, a in cfaqs)
    rel = ''.join(f'<li><a href="{u}">{t}</a></li>' for u, t in related)
    wa_msg = plain(short).replace(' ', '%20').replace('&', 'and')
    return head(title, desc, path, ld) + header(False) + f'''
<main id="main">
<div class="page-head"><div class="container">
<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="./">Home</a></li><li aria-current="page">{short}</li></ol></nav>
<h1>{h1}</h1><p>{sub}</p>
</div></div>
<div class="prose course-page"><div class="container">
<figure><img src="images/centre/{img}.webp" srcset="images/centre/{img}-480.webp 480w, images/centre/{img}.webp {img_w}w" sizes="(max-width:900px) 100vw, 860px" width="{img_w}" height="{img_h}" alt="{alt}" fetchpriority="high"><figcaption>{cap}</figcaption></figure>
{body}
<div class="course-cta">
<h2>See a class before you decide</h2>
<p>Book a free demo class. Tell us the class and board, and we will fix a convenient time.</p>
<a class="btn btn-yellow" href="tel:+919731045709">Call 097310 45709</a>
<a class="btn btn-wa" href="https://wa.me/919731045709?text=Hi%2C%20I%20would%20like%20to%20know%20about%20{wa_msg}%20tuition" target="_blank" rel="noopener">{wa}WhatsApp us</a>
</div>
<h2>Questions parents ask</h2>
{faq_html}
<p><b>A note on results:</b> we do not guarantee marks, ranks or admission. Results depend on each student's effort. See our <a href="disclosures.html">disclosures</a> for teacher qualifications, fees and refunds.</p>
<h2>Other courses</h2>
<ul class="related">{rel}</ul>
</div></div>
</main>
''' + footer(False)

C89 = 'class-8-9-tuition-vijayanagar.html'
C10 = 'class-10-tuition-vijayanagar.html'
PUC = 'puc-tuition-vijayanagar.html'

class89 = course_page(C89, 'Class 8 &amp; 9 Tuition',
  'Class 8 &amp; 9 Tuition in Vijayanagar | Smart Tutorials',
  'Class 8 and 9 tuition for ICSE, CBSE and State students in Vijayanagar II Stage, Bengaluru. Maths, Science, languages, regular tests and a free demo class.',
  'Class 8 &amp; 9 Tuition in Vijayanagar, Bengaluru', 'For ICSE, CBSE and State students, at 9th Main Road, Vijayanagar II Stage',
  'classroom', 960, 720, 'Rows of wooden benches in a classroom at Smart Tutorials, Vijayanagar', 'A classroom at our Vijayanagar centre.', f'''
<p>Maths gets more abstract in Class 8 and 9, and Science starts to split into Physics, Chemistry and Biology. A topic missed now often comes back in Class 10, when there is far less time to go over it again. Our Class 8 and 9 batches help students catch those gaps early, while there is still room to work on them calmly.</p>
<h2>Is your child ready for this kind of support?</h2>
<p>Tuition tends to help most when you notice one of these at home:</p>
<ul>
<li>Marks have started slipping in one subject, even though the others are fine</li>
<li>Your child can follow the class but gets stuck on homework alone</li>
<li>Questions pile up because they feel shy to ask at school</li>
<li>Preparation starts only a day or two before each test</li>
</ul>
<h2>What we teach</h2>
<div class="tbl"><table>
<tr><th scope="col">Area</th><th scope="col">Subjects</th></tr>
<tr><td>Maths &amp; Science</td><td>Mathematics, Physics, Chemistry, Biology</td></tr>
<tr><td>Humanities</td><td>Social Science</td></tr>
<tr><td>Languages</td><td>English, Kannada, Sanskrit</td></tr>
<tr><td>Other</td><td>Computer Applications, as per syllabus</td></tr>
</table></div>
<p>We cover ICSE, CBSE and State syllabus. ICSE students should note that the Class 10 ICSE exam is based on a two-year course, so Class 9 work counts directly towards it.</p>
<h2>How classes work</h2>
<ul>
<li><b>Regular tests</b> show students which topics they have understood and which need another look.</li>
<li><b>Doubt clearing</b> gives shy students a comfortable place to ask.</li>
<li><b>One-to-one sessions</b> are available when a student needs extra help in one subject.</li>
<li><b>Batch timings</b> are planned around school hours. Call us for the current timing.</li>
</ul>
''', [
  ('Should my child start tuition in Class 8, or wait for Class 10?', 'It depends on the child. If one subject is already difficult, starting earlier usually means fewer gaps to fill in Class 10. If school is going well, you may not need it yet. A free demo class can help you decide.'),
  ('Can my child join for only one subject?', 'Please call us on 097310 45709. We will tell you which subject batches are running and whether a one-to-one session would suit better.'),
  ('Do you teach all three boards together?', 'We cover ICSE, CBSE and State syllabus. Tell us your child\'s board when you enquire, and we will explain how the batch works for it.'),
], [(C10, 'Class 10 Tuition'), (PUC, 'PUC Tuition')])

class10 = course_page(C10, 'Class 10 Tuition',
  'Class 10 Tuition in Vijayanagar, Bengaluru | Smart Tutorials',
  'Class 10 tuition for SSLC, CBSE and ICSE students in Vijayanagar II Stage, Bengaluru. Special board-year coaching, regular tests and a free demo class.',
  'Class 10 Tuition in Vijayanagar, Bengaluru', 'Special coaching for SSLC, CBSE and ICSE students',
  'tests', 960, 540, 'Students writing a test at desks at Smart Tutorials, with faces blurred for privacy', 'Students writing a test at our centre. Faces are blurred for privacy.', f'''
<p>For most students, Class 10 is the first board exam, and it can feel like a big step for the whole family. Our Class 10 batches give students a steady routine for the year: subject coaching, regular tests, revision, and time to clear doubts before they turn into exam-day worries.</p>
<h2>Boards we cover</h2>
<div class="tbl"><table>
<tr><th scope="col">Syllabus</th><th scope="col">Board exam conducted by</th></tr>
<tr><td>SSLC (State)</td><td>Karnataka School Examination and Assessment Board (KSEAB)</td></tr>
<tr><td>CBSE</td><td>Central Board of Secondary Education</td></tr>
<tr><td>ICSE</td><td>Council for the Indian School Certificate Examinations (CISCE)</td></tr>
</table></div>
<h2>Subjects</h2>
<p>Mathematics, Physics, Chemistry, Biology, Social Science, English, Kannada, Sanskrit and Computer Applications, as per your child's syllabus. Call us to confirm the batches running this year.</p>
<h2>How the board year works here</h2>
<ul>
<li><b>Regular tests</b> build the habit of writing answers on time, not just reading them.</li>
<li><b>Revision</b> goes back over the chapters students find hardest.</li>
<li><b>Doubt clearing</b> lets students ask until the topic is clear.</li>
<li><b>One-to-one sessions</b> are available for extra help in a weak subject.</li>
</ul>
<h2>Five questions to ask any Class 10 tuition</h2>
<p>Whether you choose us or another centre, these help you compare properly:</p>
<ul>
<li>Who teaches each subject, and what are their qualifications?</li>
<li>How often are tests held, and how will I hear about the marks?</li>
<li>How does this batch handle my child's board?</li>
<li>When does revision start, and what happens if my child misses a class?</li>
<li>Can I get the fee and refund terms in writing before I pay?</li>
</ul>
''', [
  ('When should a Class 10 student join tuition?', 'As early in the year as you can, because there is more time to fix weak topics. Students can also enquire mid-year. Call us to check which batches have room.'),
  ('Is there a separate batch for SSLC, CBSE and ICSE?', 'Please call us on 097310 45709 for this year\'s batch details. Tell us your child\'s board and subjects, and we will explain how classes work for them.'),
  ('Can my child try a class first?', 'Yes, a free demo class is available. Call or WhatsApp us and we will fix a convenient time.'),
], [(C89, 'Class 8 &amp; 9 Tuition'), (PUC, 'PUC Tuition')])

puc = course_page(PUC, 'PUC Tuition',
  'PUC Tuition in Vijayanagar, Bengaluru | Smart Tutorials',
  'I PUC and II PUC tuition in Vijayanagar II Stage, Bengaluru. Subject-wise coaching, regular tests and doubt clearing. Call 097310 45709 for current batches.',
  'PUC Tuition in Vijayanagar, Bengaluru', 'Coaching for I PUC and II PUC students',
  'office', 960, 720, 'A staff member working at a desk in the Smart Tutorials office, Vijayanagar', 'Our office at the Vijayanagar centre.', f'''
<p>I PUC and II PUC, the Karnataka equivalent of Class 11 and 12, are a real jump from high school. Chapters are longer, concepts go deeper, and college timings leave less room for catching up alone. Our PUC coaching gives students a fixed place to work through their subjects, take regular tests and ask questions.</p>
<h2>Tell us your combination</h2>
<p>PUC students take different subject combinations, such as PCMB or PCMC, so the first step is simple: call us with your stream, subjects and college timing. We will tell you honestly which subjects and batches are running now.</p>
<h2>How classes work</h2>
<ul>
<li><b>Subject-wise coaching</b> focuses on the subjects you need help with.</li>
<li><b>Regular tests</b> keep preparation steady through the year, not only before exams.</li>
<li><b>Doubt clearing</b> gives you time to ask about what you did not follow in college.</li>
<li><b>One-to-one sessions</b> may be available when you need extra help in one subject.</li>
</ul>
<h2>Getting ready for I PUC</h2>
<p>If you have just finished Class 10, the weeks before college are a good time to get ahead. Revise the Class 10 chapters that PUC builds on, especially in Maths and Science, and look through your new textbooks. Starting college with fewer gaps makes the first few months much easier.</p>
''', [
  ('Do you coach both I PUC and II PUC?', 'Yes, our centre takes PUC students. Subjects and batches can change each year, so please call us on 097310 45709 to confirm what is running now.'),
  ('Will the timings clash with college?', 'Batches are planned around school and college hours. Share your college timing when you call, and we will tell you what fits.'),
  ('Can I attend a demo class first?', 'Yes, a free demo class is available. Call or WhatsApp us to fix a time.'),
], [(C89, 'Class 8 &amp; 9 Tuition'), (C10, 'Class 10 Tuition')])

course_pages = [(C89, class89), (C10, class10), (PUC, puc)]

for name, html in [('index.html', index()), ('privacy.html', privacy), ('terms.html', terms), ('disclosures.html', disclosures), ('404.html', nf)] + course_pages:
    open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n').write(html)
open(os.path.join(OUT, 'robots.txt'), 'w', newline='\n').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
urls = ''.join(f'  <url><loc>{SITE}/{p}</loc><lastmod>2026-11-04</lastmod></url>\n' for p in ['', 'class-8-9-tuition-vijayanagar.html', 'class-10-tuition-vijayanagar.html', 'puc-tuition-vijayanagar.html', 'disclosures.html', 'privacy.html', 'terms.html'])
open(os.path.join(OUT, 'sitemap.xml'), 'w', newline='\n').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
print('built')
