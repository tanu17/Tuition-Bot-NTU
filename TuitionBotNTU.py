import sys
import telepot
from telepot.delegate import pave_event_space, per_chat_id, create_open
import time, os, pickle


#the program basically inputs details from user, their name ,year,school which they have problem in,course which they have problem in and finally he topic which they have problem in
#the __next__ step will be to have a tutor enter their details and finally match tutor and student by exchanging their informations
#and if possible to xreate a new bot for them so that both of them can chat

class MessageCounter(telepot.helper.ChatHandler):
    


    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self.s=""               #created so that message list to be send can be send in one message only and not in messsages
        self.teacher_stu=""     #stores whether the user is a student or teacher (not used for admin)
        self.s1=""              #created so that message list to be send can be send in one message only and not in messsages
        self.count = 0       #counter in the program
        self.name=""            #stores name of user
        self.school="scse"      #stores school of user(not used for admin)
        self.course_study=""    #stores the course chosen(not used for admin)
        self.content_study=""   #stores the content of study chosen(not used for admin)
        self.year=0             #stores the year of student/teacher(not used for admin)
        self.__password="q"     #passwword for admin(stored as private variable)
        self.file_no=""         #input for admin to see details of a user
        self.__phone=""         # stores phone no as private variable in form oof string
        self.match=0
        self.teacher_list=[]    #stores information of students till now
        self.student_list=[]    #store info about teacher till now
        self.current_no_of_files #stores no of users till now
        

        #database for courses and course content(with no indicating year of study/teaching)

        self.course_scse1=['Introduction To Computing Systems','Introduction To Computational Thinking', 'Inventions And Innovations In Computing', 'Digital Logic', 'Computer Organisation And Architecture', 'Data Structures', 'Engineering Mathematics I', 'Engineering Mathematics II', 'Engineers And Society', 'Discrete Mathematics']

        self.course_scse2=['Algorithms', 'Object Oriented Design And Programming', 'Digital Systems Design', 'Circuits And Signal Analysis', 'Operating Systems', 'Software Engineering', 'Microprocessor-based Systems Design']

        self.course_scse3=['Advanced Computer Architecture', 'Sensors, Interfacing And Control', 'Sensors, Interfacing And Control', 'Multidisciplinary Design Project (Mdp)', 'Computer Networks', 'Digital Communications', 'Digital Signal Processing']

        self.course_scse4=['Virtual And Augmented Reality', 'Visual Media Compression And Processing', 'Computer Vision', '3d Modeling And Animation', 'Audio And Speech Processing', 'Parallel Computing', 'Distributed Systems', 'Simulation And Modelling', 'Advanced Topics In Algorithms', 'Pervasive Networks', 'Personal Mobile Networks', 'Advanced Computer Networks', 'Cryptography And Network Security', 'Embedded Systems Design', 'Embedded Systems Development', 'Embedded Operating Systems', 'Programmable Systems-on-chip', 'Computer Security (System Security)', 'security Management', 'Digital Forensics']


        #course content stored in the form of nested list

        self.content_scse1=[['Introduction','Computer Pioneers and their contributions', 'Evolution of Computers – Part I', 'Basic CPU operation and programming language evolution', 'Evolution of Computers– Part II', 'CPU Performance Enhancement techniques', 'Programming Languages', 'Programming Paradigms', 'The internet', 'Networks and communications', 'Multi-tasking and Operating Systems', 'Classifications of Computer Systems', 'Computing Trends', 'The Database', 'e-learning'],['Computing and Algorithms', 'Introduction to Python', 'Basic syntax and meaning', 'Variables, Data types, and Operators', 'More on numbers and built-in functions', 'Flow control', 'Program Development Issues (supplementary)', 'Strings ancocharacter access', 'Composite types', 'User defined functions and modules', 'File management', 'Exceptions'],['Binary operations', 'Von Neumann and Harvard architectures', 'Invention of semiconductor materials', 'Examples of simple and complex CPUs', 'Programming Paradigms and Languages', 'Compilers and Algorithms', 'Operating Systems', 'Internet and distributed computing', 'Social networks', 'Numerical methods for the approximate computer solution of otherwise intractable problems', 'Databases', 'Data Analytics', 'Computer graphics and animation', 'Graphics Processor Unit', 'Computer and data security', 'Program Verification, Testing, Reliability and Correctness'],['Binary integers and arithmetic', 'Boolean Variables and Logic', 'Combinatorial circuits', 'Implementation technologies', 'Digital design using hardware description languages', 'Sequential circuits', 'Sequential circuits to building blocks', 'Finite state machines'],['Computer Hardware Decomposition', 'Data Representation, Memory Allocation and Access', 'Central Processing Unit', 'Assembly Programming and Instruction Set Architecture', 'High-level Software to Low-level Instructions', 'Computer Memory', 'Data Transfer and Input/Output (I/O) Techniques', 'Computer Arithmetic', 'Measuring system performance', 'Towards higher speed'],['Basic Constructs in CC program structure', 'Syntax and semantics', 'Built-in Data Structures', 'Recursion', 'Memory Management in C', 'Linked Lists', 'Stacks and Queues', 'Tree Structures', 'Implementing other data abstractions'],['Complex Numbers', 'Vectors', 'Matrices', 'Systems of Linear Equations', 'Descriptive statistics', 'Probability theory', 'Probability and sampling distributions', 'Inferential statistics', 'Experimental and Numerical Methods'],['Precalculus', 'Limits and Continuity', 'Differentiation', 'Integration', 'Ordinary Differential Equations (ODE)', 'Sequences and Series', 'Function approximation', 'Numerical diffeinvalid ansrentiation and integration', 'Fourier Series', 'Fourier Transform'],['Issues pertinent to engineers as professionals as well as members of society', 'Requirements and issues of the IT profession', 'Key role professionals play with their contributions to society', 'Current concerns of any person living in Singapore'],['Elementary number theory', 'Propositional logic', 'Predicate logic', 'Proof techniques', 'Sets', 'Linear recurrence relation', 'Relations', 'Functions', 'Graphs', 'Elementary Combinatorics']]

        self.content_scse2=[['Introduction to algorithms', 'Analysis of algorithms', 'Sorting', 'Searching', 'Graphs', 'Basic Computability and Complexity Theory'],['Introduction to Object Orientated Programming', 'Classes and Objects', 'C++ Programming Language', 'Inheritance and polymorphism', 'Interface and implementation', 'Object Relationships', 'Object Collaboration', 'Designing for Reuse', 'Java Programming Language', 'Persistent Objects'],['Review of Verilog and the Digital Design Flow', 'Verification and Testing', 'Arithmetic Design', 'FPGA Architecture and Synthesis', 'Timing, Pipelining, and Scheduling', 'Subsystem Design', 'Busses and Interfacing', 'Fundamentals of Asynchronous Circuits'],['DC Signal Analysis', 'AC Signal Analysis', 'Signals and Systems', 'Active Circuit Elements'],['Overview of Operating Systems (OS)', 'Processes and Threads', 'Process Scheduling', 'Process Synchronization', 'Deadlock and Starvation', 'Memory Organization', 'Virtual Memory Management', 'File System Organization and Implementation', 'Input/Output (I/O) Management and Disk Scheduling', 'Issues in Real-time Operating Systems', 'Protection and Security'],['Introduction to Software Engineering', 'Requirement Specification', 'Analysis', 'Project Management', 'Design', 'Implementation and Testing', 'Maintenance'],['Microprocessor landscape', 'Microprocessor packages, signals and interfacing – Part 1', 'Introduction to ARM Cortex-M Architecture and Programming', 'Peripherals, interfaces and applications – Part 1', 'Analog signal conditioning and Interfacing', 'Displays', 'Signals and interfacing – Part 2', 'Peripherals, interfaces and applications – Part 2', 'Semiconductor memory technology and characteristics', 'Fabrication', 'System Design Issues', 'Further integration and programming']]

        self.content_scse3=[['Introduction and Background', 'Review of basic computer architecture', 'Instruction Set Architecture Design', 'Micro-architecture Design', 'Memory Systems and I/O Design', 'Instruction-Level Parallelism', 'Data-Level Parallelism', 'Thread-Level Parallelism', 'Emerging Computing Trends'],['Overview of electronic instrumentation and control systems', 'Transducers', 'Signal Conditioning Circuits', 'Amplifier circuits', 'Filter circuits', 'Op-Amp specifications', 'Signal conditioning circuit design', 'Digital Interfaces', 'Introduction to control system', 'z-transform', 'Transfer function', 'Design of Digital Control', 'Linear Discrete Data System'],['lntegrated Development Environments', 'Microcontroller Architectures', 'Efficient Real-time "C" Programming Techniques', 'Linking "C" with Assembler and Libraries', 'Programming Peripherals and Subsystems', 'Handling Multiple Tasks in Real-Time', 'Real-Time Operating Systems', 'Compiler optimizations'],['Microprocessors, Signals and Interfaces', 'Sensors and Communication', 'Software engineering', 'Data structures and Algorithms', 'Open-source frameworks', 'Human-computer interaction', 'System analysis and design'],['Computer Network Concepts', 'Network Types and Performances', 'Data Link Layer', 'Local Area Networks', 'Network Layer', 'Transport Layer', 'Application Layer'],['Introduction', 'Signals and Spectra', 'Baseband Modulation, Demodulation/Detection', 'Band-pass Modulation, Demodulation/detection', 'Source Coding', 'Channel Coding', 'Challenges in Communication System Design'],['Discrete-time Signals and Systems', 'Frequency Analysis of Signals and Systems', 'The Discrete Fourier Transform', 'Sampling and Reconstruction', 'FIR and IIR Filter Design, Digital Filter Structure']]

        self.content_scse4=[['Introduction', 'Graphical Scene', 'Animation and Sensing', 'Light and Sound', 'Controlling Environment', 'Programming Scripts', 'Introduction to Augmented Reality', 'Displays for Augmented Reality', 'Tracking, Recognition and Registration', 'Rendering and Augmentation', 'Examples of Augmented Reality System'],['Introduction to media management & processing', 'Entropy coding', 'Digital image coding techniques', 'Motion Estimation', 'Digital video coding techniques', 'Advanced topics for visual signal compression', 'Content Base Image retrieval'],['Introduction to computer vision', 'Principles of Camera Systems', 'Image Enhancement in the Spatial domain', 'Image Enhancement in the Frequency domain', 'Colour', 'Edge Processing', 'Region Processing', 'Imaging Geometry', '3D Stereo Vision', 'Object Recognition'],['Introduction', 'Computer Graphics Pipeline', 'Graphics Programming', '3D Shape Representation', 'Geometric Processing', 'Rendering', 'Basic Animation Techniques', 'Kinematic Animation', 'Physics Based Simulation', 'Motion Capture'],['Introduction', 'Speech Production and Transcription', 'Audio Signal Analysis', 'Audio and Speech Signal Classification', 'Text to Speech Synthesis', 'Speaker Recognition/Verification'],['Foundations & Theory', 'Distributed Memory Programming', 'Shared Memory Programming', 'Special ELearning Topic, Load Balancing', 'Massively Parallel Programming', 'Cases Studies'],['Characteristics of distributed systems and system models', 'Interprocess communication', 'Distributed objects and remote invocation', 'Distributed file systems', 'Peer-to-peer systems', 'Name services', 'Time and global states', 'Coordination and agreement', 'Replication and consistency'],['Introduction', 'Different Types of Simulation', 'Simulation World View and Simulation Software', 'Basic Probability and Statistical Models for Simulation', 'Random Numbers and Random Variate Generation', 'Input Modelling', 'Verification and Validation of Simulation Models', 'Output Analysis', 'Comparison of Alternative Designs', 'Queueing Models'],['Analysis Techniques', 'Dynamic Programming', 'Search Techniques', 'Computational Geometry', 'Min Cut /Max Flow', 'Lower Bounds and NP-completeness', 'Approximation Algorithms and Heuristics', 'Randomized Algorithms'],['Introduction of Pervasive Networks', 'Medium Access Control (MAC) for Wireless Networks', 'Routing in Mobile Ad Hoc Networks (MANETs)', 'Mobility Management Services in Cellular Networks', 'Mobile Internet Protocol (IP)'],['Fundamentals of Wireless Mobile Communications', 'Overview of mobile networks, Wireless Personal Area Networks (WPAN)', 'Wireless Local Area Networks (WLAN)', 'Wireless Wide Area Networks (WWAN)', 'Cellular communications networks', 'Satellite communications'],['Top-Down View of Computer Networks', 'Application Layer Protocols', 'Multimedia Networking', 'Advanced Network Protocols', 'QoS and Traffic Management', 'Network Deployment and Design'],['Security Threats and Security Goals', 'Mathematical Background', 'Secret-Key Cryptography', 'PublicKey Cryptography', 'Hash Functions and MACs', 'Key Management', 'Authentication Protocols', 'Key Establishment Protocols'],['What is Design', 'Meeting Design Constraints', 'Software Design (Modeling)', 'Software Design (Analysis)', 'Hardware Design (Modelling)', 'Hardware Design (Implementation)', 'Sensors and I/O Hardware/Software Co-Design', 'Hardware/Software Co-Design (Case study)'],['Introduction to Embedded Systems Programming', 'The Android Ecosystem', 'Software Design and Management', 'Profiling & Optimization', 'Hardware Acceleration', 'Multi-Threading', 'Scheduling & Prioritisation', 'Advanced Topics'],['Embedded OS Introduction', 'Relevance of Embedded OS', 'Benchmarking Performance', 'Single-core Scheduling', 'Multi-core Scheduling', 'Resource/Data Sharing', 'Isolation through Virtualization', 'RTOS case-studies', 'Recent Trends'],['Intro to Programmable SoCs', 'The SoC Design Flow', 'SoC Compute Organizations', 'Communication and I/O Abstractions', 'Tuning SoCs', 'Memory Organizations', 'Advanced Optimization Topics', 'Design Space Exploration', 'SoC Project Management and Formulation'],['Introduction, Concepts, and Terminology', 'Identification and Entity Authentication', 'Access-Control', 'Security Models', 'Reference Monitors', 'Operating System Security', 'Software Security', 'Case Studies'],['Introduction', 'Information Security, Governance, and the Law', 'Model, Framework, and Approach', 'Organization and People', 'Risk Analysis and Assessments', 'Security Operations', 'Internal Control, Audit, and Security', 'Contingency Planning and Management'],['Overview of forensic science', 'Anti-Forensics', 'Host Forensics', 'Information Hiding', 'Non-Standard Storage Mechanisms and Devices', 'Network Forensics']]
        

        #database for videos in form of nested list like that of content (nested list)

        self.year1_videos=[["-"],['https://www.youtube.com/watch?v=JkZ61JEirnI','https://www.youtube.com/watch?v=rkx5_MRAV3A','https://www.youtube.com/watch?v=YFmm6e5HHeM','https://www.youtube.com/watch?v=657yt4gYjRo','https://www.youtube.com/watch?v=qrmhOajLqTQ', 'https://www.youtube.com/watch?v=4O2RG38B7nc',' ', 'https://www.youtube.com/watch?v=QbbdRHmNFFY','https://www.youtube.com/watch?v=R-HLU9Fl5ug', 'https://www.youtube.com/watch?v=cx5PNyeAsng', 'https://www.youtube.com/watch?v=sl-AGRKWhWU', 'https://www.youtube.com/watch?v=aL6fc8T-kMo'],['https://www.youtube.com/watch?v=gXxugQrrEgU', 'https://www.youtube.com/watch?v=4_oh2a2J3Y4', 'https://ww.youtube.com/watch?v=7jaa1rlW7Ak', 'https://www.youtube.com/watch?v=cNN_tTXABUA', 'https://www.youtube.com/watch?v=Z62rQwe8MSI', 'https://www.youtube.com/watch?v=fayV41SIV2w','https://www.youtube.com/watch?v=9GDX-IyZ_C8', 'https://www.youtube.com/watch?v=LkkQy6ivbe4', 'https://www.youtube.com/watch?v=fgr_g1q2ikA', 'https://www.youtube.com/watch?v=lFYzdOemDj8', 'https://www.youtube.com/watch?v=3SK9iJNYehg', 'https://www.youtube.com/watch?v=xKVS_81Op5A', 'https://www.youtube.com/watch?v=BKWFM_6fREk','https://www.youtube.com/watch?v=-yFZGF8FHSg','https://www.youtube.com/watch?v=Ayg0V1qiJwc&list=PLadvdCkEgn7ry0naFWkeFHp13Sefw_Ybb'],['https://www.youtube.com/watch?v=sFd5bnDdB3Q', 'https://www.youtube.com/watch?v=E6JE48FJ9-M','https://www.youtube.com/watch?v=pqwwcpa53PA','https://www.youtube.com/watch?v=eafualvLROs','https://www.youtube.com/channel/UCKfKzUv9Cx6cEcoOMMhI_8Q', "https://www.youtube.com/watch?v=s3wuZZ9S5pA", "https://www.youtube.com/channel/UCdXAva_TTSdXSedlVCnHv6w",'https://www.youtube.com/watch?v=LuGs7WhlHWA'],['https://www.youtube.com/watch?v=lPIXAtNGGCw&list=PL291F84A80CA32304','https://www.youtube.com/watch?v=Rnfu5qyysro', 'https://www.youtube.com/watch?v=cNN_tTXABUA', 'https://www.youtube.com/watch?v=x0gH5JGNIKg&list=PLc2rvfiptPSRxHg8idaITpBzWNcG_z7x5','https://www.youtube.com/watch?v=7OnieVsf7q0', 'https://www.youtube.com/watch?v=F0Ri2TpRBBg', 'https://www.youtube.com/watch?v=MOIGpeHVZhc','https://www.youtube.com/watch?v=o-WXqnagg0c', 'https://www.youtube.com/watch?v=m8zi9ZUfpGs','https://www.youtube.com/watch?v=mQS38ct_0z4'],['https://www.youtube.com/watch?v=bu8YRZKo9lc','https://www.youtube.com/watch?v=7Q3_LByX9Gs', 'https://www.youtube.com/watch?v=Z5jXIMT_Omk','https://www.youtube.com/watch?v=o3JABquhDZg','https://www.youtube.com/watch?v=_AGdMz08T1s','https://www.youtube.com/watch?v=pBrz9HmjFOs','https://www.youtube.com/watch?v=JvGZh_BdF-8', 'https://www.youtube.com/watch?v=qH6yxkw0u78','https://www.youtube.com/watch?v=ab82D1Vqcso'],["https://www.youtube.com/watch?v=ysVcAYo7UPI&list=PLGR_7q6BJHQGo3lIEUzEWrCLFleDRzvVM" ,'https://www.youtube.com/watch?v=jCkhbKFZgLk','https://www.youtube.com/watch?v=xyAuNHPsq-g&list=PL26BD351D91DFB72E','https://www.youtube.com/watch?v=DoW2DlGg_bk&list=PLtXf78zN40CLDf7V4abHyMccLG_X_8XHc&index=3', "https://www.youtube.com/watch?v=dbUsaozc4Fo&index=23&list=PLEjUUlEpP-BMPmG6IRIJThetDkteH4yAf",'https://www.youtube.com/watch?v=j9WZyLZCBzs&list=PLw1fyPVTTowrkyhzkc_PiItPm-S58_UQ1', 'https://www.youtube.com/watch?v=NQPCV_ml-jo&list=PLiNLu3L3qpqXlRLPjz0JIGEzJUKSh_lQe', 'https://www.youtube.com/watch?v=-FtlH4svqx4','https://www.youtube.com/playlist?list=PLpZ9d5bVHHlQeDn1BItuO1KysbDYhlR2v'],['https://www.youtube.com/playlist?list=PLE88E3C9C7791BD2D', 'https://www.youtube.com/watch?v=riXcZT2ICjA&list=PLF6B400A9E9460723','https://www.youtube.com/playlist?list=PLNBvgVuabOc-bkAkjKzrRfelViGlo_5fU','https://www.youtube.com/playlist?list=PL38226E3FEAC0B9B7', 'https://www.youtube.com/watch?v=-_POEWfygmU&list=PL96AE8D9C68FEB902',  'https://www.youtube.com/watch?v=KRFiAlo7t1E&list=PLVwvyzz17cDIyII2iy_Ho5lZU9zF6-KyZ','https://www.youtube.com/playlist?list=PLVwvyzz17cDIyII2iy_Ho5lZU9zF6-KyZ','https://www.youtube.com/playlist?list=PLYdroRCLMg5OvLx1EtY1ByvveJeTEXQd_', 'https://www.youtube.com/playlist?list=PL1B727B06A221E026',"https://www.youtube.com/playlist?list=PLUMWjy5jgHK3jmgpXCQj3GRxM3u9BmO_v"],['https://www.youtube.com/watch?v=qUnzyzjrOBA','-','https://www.youtube.com/watch?v=RVlvkHm5NQM','https://www.youtube.com/watch?v=EQGTNyw9Rmk'],['https://www.youtube.com/playlist?list=PLtvClhypCw9mP_rTWakp1JsqpxR3s6rQ2', 'https://www.youtube.com/playlist?list=PL619166130C21EADA','https://www.youtube.com/playlist?list=PLEHmI0Qx0uPlVgI7xMmB_S1iuHOe9EX0f', 'https://www.youtube.com/watch?v=YFZzLQN5qOU&list=PLnxogSzcUqJcjIUxUGZLTUfAIkeIjEFJq','https://www.youtube.com/watch?v=5plFb4jrzd4&list=PLDDGPdw7e6Ag1EIznZ-m-qXu4XX3A0cIz','https://www.youtube.com/watch?v=nKnNJ3It1IY&list=PLDC6AhaFBoXMR4B5Ogi54skcvchllHPq-&index=3', 'https://www.youtube.com/watch?v=XfpfijZss8Y&list=PLtvClhypCw9kcASFi7jYnplcf3JGewE_K', 'https://www.youtube.com/playlist?list=PLSAYJlB7VGWSVqmW5_8ONESxeLIQt7dm1','https://www.youtube.com/playlist?list=PLW3Tw6vi-WwD1Z5afG-L7A5HunzZ-swkk',"https://www.youtube.com/watch?v=MKJw_q1sJgo&index=33&list=PLa8a_8vztYc5NM2jTl9ZPgkVS76ibLKjG"]]
        
        self.year2_videos=[['https://www.youtube.com/watch?v=JPyuH4qXLZ0&hl=en-GB&gl=SG','https://www.youtube.com/watch?v=2P-yW7LQr08&list=PLUl4u3cNGP6317WaSNfmCvGym2ucw3oGp','https://www.youtube.com/watch?v=Nz1KZXbghj8','https://www.youtube.com/watch?v=9Jry5-82I68','https://www.youtube.com/watch?v=gXgEDyodOJU','https://www.youtube.com/watch?v=moPtwq_cVH8'],['https://www.youtube.com/watch?v=lbXsrHGhBAU','https://www.youtube.com/watch?v=lbXsrHGhBAU','https://www.youtube.com/watch?v=S3t-5UtvDN0','https://www.youtube.com/watch?v=ng98qapa4Sw','https://www.youtube.com/watch?v=v4SdA2ehvoU','https://www.youtube.com/watch?v=kZnaFP9U9nY','https://www.youtube.com/watch?v=RcZAkBVNYTA','https://www.youtube.com/watch?v=ZQ5_u8Lgvyk','https://www.youtube.com/watch?v=3u1fu6f8Hto','https://www.youtube.com/watch?v=znnAMcGfI0E'],['https://www.youtube.com/watch?v=0age83XI8Z4 ; https://www.youtube.com/watch?v=5-EEAB0XUIk','https://www.youtube.com/watch?v=5-EEAB0XUIk','https://www.youtube.com/watch?v=5-EEAB0XUIk','https://www.youtube.com/watch?v=CLUoWkJUnN0','https://www.youtube.com/watch?v=rHtNQTjOY3E','https://www.youtube.com/watch?v=AXgfeV568c8','-','https://www.youtube.com/watch?v=Ss1Saa54sBI','https://www.youtube.com/watch?v=AVrJRPL-e0g'],['https://www.youtube.com/watch?v=3ARwItoY_nc','https://www.youtube.com/watch?v=3ARwItoY_nc','https://www.youtube.com/watch?v=-FHm2pQmiSM&list=PLUl4u3cNGP61kdPAOC7CzFjJZ8f1eMUxs','https://www.youtube.com/watch?v=JAX4xARloXk'],['https://www.youtube.com/watch?v=JAX4xARloXk','https://www.youtube.com/watch?v=hsERPf9k54U','https://www.youtube.com/watch?v=FiGKndlvO8I','https://www.youtube.com/watch?v=FiGKndlvO8I','https://www.youtube.com/watch?v=2klwq4GeVtw','https://www.youtube.com/watch?v=0FPOgQ5_YZk','https://www.youtube.com/watch?v=iqfjWIYyQ9k','https://www.youtube.com/watch?v=a86Nxi7lH1s','https://www.youtube.com/watch?v=WW2vB_e-8Os','https://www.youtube.com/watch?v=HlU5cYqGLZE','https://www.youtube.com/watch?v=6nadXMSFSjk'],['https://www.youtube.com/watch?v=LOLxYo23KLc','https://www.youtube.com/watch?v=wEr6mwquPLY','https://www.youtube.com/watch?v=wEr6mwquPLY','https://www.youtube.com/watch?v=1TxXtrQRkuw','https://www.youtube.com/watch?v=1TxXtrQRkuw','https://www.youtube.com/watch?v=Zmv6ha2IBtE','https://www.youtube.com/watch?v=8CO29Pbyjx0'],['https://www.youtube.com/watch?v=1famitdmzwk&list=PLZ9YeF_1_vF-y4pIbimAX8iyLJhPjCeLl','https://www.youtube.com/watch?v=ssc-i-Vl3iM','https://www.youtube.com/watch?v=7LqPJGnBPMM','https://www.youtube.com/watch?v=9A5ivudtfsw','https://www.youtube.com/watch?v=Chw-FmmDh2I','https://www.youtube.com/watch?v=jxX8MexaVTk','https://www.youtube.com/watch?v=JJqraszIeeU','https://www.youtube.com/watch?v=9A5ivudtfsw','https://www.youtube.com/watch?v=omxQsvenf9o','https://www.youtube.com/watch?v=UhJ5op0WZLg','https://www.youtube.com/watch?v=whYljse4Abc','-']]
        
        self.year3_videos=[['https://www.youtube.com/watch?v=39LjZM2zMMw','Instead of seeing a video ,it would be better if you could refer the notes','https://www.youtube.com/watch?v=HbsuwpJgKao','https://www.youtube.com/watch?v=NrfuKTGvsFE','https://www.youtube.com/watch?v=ZSw5HPUwK8s','https://www.youtube.com/watch?v=BWmljynuhYo','https://www.youtube.com/watch?v=LFHOMYlWslU','https://www.youtube.com/watch?v=TfIajPoRdmw','https://www.youtube.com/watch?v=Q-1mSk0HYuY'],['https://www.youtube.com/watch?v=jnY9T4Bf9h8','https://www.youtube.com/watch?v=xaOF2SNktRY','https://www.youtube.com/watch?v=Rje5DJSe098','https://www.youtube.com/watch?v=WT-qzgaKeGI','https://www.youtube.com/watch?v=IEeltuxzPYE','https://www.youtube.com/watch?v=VtxFtzWlTgg','https://www.youtube.com/watch?v=dP496kJmzXc','https://www.youtube.com/watch?v=o1MWMrFhXXs','https://www.youtube.com/watch?v=O-OqgFE9SD4&list=PLFFbyVlrhQnvaEyHXkfxpKRVzhDocc6eT','https://www.youtube.com/watch?v=NjRiqHSGmB0','https://www.youtube.com/watch?v=RJleGwXorUk','https://www.youtube.com/watch?v=rNMlaq8xABE','https://www.youtube.com/watch?v=eNVN67eZC88'],['https://www.youtube.com/watch?v=o-a1uXkcNXY','https://www.youtube.com/watch?v=pz57y4BHIy0','http://www.open-std.org/jtc1/sc22/wg21/docs/ESC_Boston_01_304_paper.pdf','https://www.youtube.com/watch?v=I35w8v_rcmY','https://www.youtube.com/watch?v=kgcUVZARftQ','https://www.youtube.com/watch?v=oWmTJdYYRTg','https://www.youtube.com/watch?v=FnGCDLhaxKU'],['-'],['https://www.youtube.com/watch?v=JvXro0dzJY8','https://www.youtube.com/watch?v=EcbyD_YycPA','https://www.youtube.com/watch?v=0nUERzTBJbQ','https://www.youtube.com/watch?v=t9TmvFvYfWw','https://www.youtube.com/watch?v=V3E1LmPtkDk','https://www.youtube.com/watch?v=TKJ5oobqcE0','https://www.youtube.com/watch?v=0_QczZ1lNDU'],['https://www.youtube.com/watch?v=3w_0163BVQk','-','https://www.youtube.com/watch?v=I0Xz0ORXkVM','https://www.youtube.com/watch?v=lYjIGni4Z7g','https://www.youtube.com/watch?v=g4FHG04Yra8','https://www.youtube.com/watch?v=lYjIGni4Z7g','https://www.youtube.com/watch?v=nDPoMPT1dYY','https://www.youtube.com/watch?v=eOMpGda71Fg','https://www.youtube.com/watch?v=whYljse4Abc'],['https://www.youtube.com/watch?v=LJ--VtkMxQY','https://www.youtube.com/watch?v=_0bxZCiFZpU&list=PLdciPPorsHukq1koI2EsNpKir3j0lKkCn','https://www.youtube.com/watch?v=GDFTb-BwA0o','https://www.youtube.com/watch?v=FLPqshreE-g','https://www.youtube.com/watch?v=9yNQBWKRSs4','https://www.youtube.com/watch?v=Z1N0qeiw9oE']]

        self.year4_videos=[['https://www.youtube.com/watch?v=H03G8Y7C9L0','https://www.youtube.com/watch?v=zvgWgpGZVKc','http://www.tandfonline.com/doi/abs/10.1080/088395199117315','-'],['-'],['https://www.udacity.com/course/introduction-to-computer-vision--ud810'],['Resources can be found at - http://www.comp.nus.edu.sg/~kkyin/CS3242/'],['https://www.youtube.com/watch?v=Xjzm7S__kBU'],['https://www.youtube.com/watch?v=yUtn_vUPbNg&list=PL5PHm2jkkXmh4cDkC3s1VBB7-njlgiG5d'],['https://www.youtube.com/watch?v=7zafB2GkMBk&list=PL72C36006AD9CED5C'],['https://www.youtube.com/watch?v=d3ChB1tDMyI&list=PLUl4u3cNGP63eWjy1orBicyAXrunfs2jT'],['https://www.youtube.com/watch?v=0JUN9aDxVmI'],['https://www.youtube.com/watch?v=t9rF051DWkk'],['http://www.cse.wustl.edu/~jain/cse574-10/'],['-'],['https://www.youtube.com/watch?v=WGmvE9ns4nM&list=PLPl8TJzokTObVRv1Mwo-hP_UV0S1GpUzf'],['https://www.youtube.com/watch?v=9oorSIfCR5I&list=PLQefpK95HyFmao3zi-WDOMkeSev-Je5dE'],['https://www.youtube.com/watch?v=3V9eqvkMzHA&list=PLPW8O6W-1chwyTzI3BHwBLbGQoPFxPAPM'],['https://www.youtube.com/watch?v=bOFMXuoc5kE&list=PLsiW6hTaeDlSerwQ6JYAu2ED7b4nsMBHM'],['https://www.youtube.com/watch?v=pFz1S5NVfRg&list=PLlBhKdf4iTIhzXN0qFK6DKDHHtUsc301S'],['https://www.youtube.com/watch?v=GqmQg-cszw4&list=PLUl4u3cNGP62K2DjQLRxDNRi0z2IRWnNh'],['https://www.youtube.com/watch?v=V7T4WVWvAA8&list=PL5E6D4A5B33DCAE78'],['https://www.youtube.com/watch?v=Gt0JyXxfB2E&list=PL6oHuo5it4TgA-ZtIo3x5G0l0HDwPPZ9d']]


    ## input from user(count 2-6) , output and confirm of content that was chosen by user (count 7) ,  making a new file (count 8) ,matching (count 9) ,adminstrator functions (count 11-12)  , checking if match is available (count 10) , thank you message and video if available (count 12)

    def on_chat_message(self, msg):



         #command for entering name
        self.useless=msg['text']        #to initiate chat ,user enters any key,which is not stored and whicch doesnt have any use on the program.Hence the first message is useless

        if self.count==0:

            if not os.path.exists(".\\TuitionBot_Users"):
                # Making said folder if not found
                os.mkdir(".\\TuitionBot_Users")
            (root, dir, files) = os.walk(".\\TuitionBot_Users").__next__()
            files.sort()
            self.current_no_of_files=len(files)
            for i in range (len(files)):
                file_2_list = open(".\\TuitionBot_Users\\" + files[i], "rb")
                (name,teacher_stu,year,content_study,course_study,phone)= pickle.load(file_2_list)
                if teacher_stu=="s":
                    self.student_list.append([i+1,content_study])
                elif teacher_stu=="t":
                    self.teacher_list.append([i+1,content_study])
                file_2_list.close()    
            self.count+=1


        if self.count==1:       

            self.sender.sendMessage("Welcome \n Enter your name please")
            self.count+=1
            

        #command for entering whether user student or teacher or admin
        elif self.count==2:        

            self.name=msg['text']                                                       
            self.sender.sendMessage("Name:" + self.name+"\n\nAre you  \n1.student  \n2.teacher  \n3.admin")
            self.count+=1
            print("name:",self.name)

        #command for entering which year course to choose and chosing value of count accordingly(could take all possible choices entered like 3 or admin or 3.admin or 3. in upper or lower case and will still work)
        elif self.count==3:

            self.teacher_stu=msg['text']
            if self.teacher_stu.lower() in ["1","1.","student","1.student"]:
                self.teacher_stu="s"
                self.sender.sendMessage("Which year are you in:\n1\n2\n3\n4")               
                self.count+=1
            elif self.teacher_stu.lower() in ["2","2.","2.teacher","teacher"]:
                self.teacher_stu="t"
                self.sender.sendMessage("Select which year courses you would like to teach: \n1\n2\n3\n4")
                self.count+=1
            elif self.teacher_stu.lower() in ["3","3.","admin","3.admin"]:
                self.sender.sendMessage("Enter password:")
                self.count=11
            else:
                self.sender.sendMessage("The input you entered was wrong.\nDont worry you still get to correct yourself")
                self.count=2
            print(self.teacher_stu)    

        elif self.count==4:   

            if self.teacher_stu=="s" or "t":                                  
                self.year=int(msg['text'])                             
                self.count+=1
                self.sender.sendMessage("Enter your phone number (so that you can contact a fellow student/teacher)\nNOTE:phone number should be standard singapore 8 digit number")
          
            else:
                self.sender.sendMessage("The input you entered was wrong.\nDont worry you still get to correct yourself")
                self.count=3
            

        elif self.count==5:

            self.__phone=msg['text']

            if  len(self.__phone)==8:
                if self.teacher_stu=="s":
                    self.s="Select the course number you have problem in: \n "         #Asking which course to choose
                elif self.teacher_stu=="t":
                    self.s="Select the course number you would like to teach: \n"

                if self.year==1:  
                    
                    for i in range (len(self.course_scse1)):
                        self.s+=str(i+1)+") "+self.course_scse1[i]+"\n"
                    self.s+="\nRemember to input number only"
                    self.sender.sendMessage(self.s)                   
                    self.count+=1
  

                elif self.year==2:  

                    for i in range (len(self.course_scse2)):
                        self.s+=str(i+1)+":"+self.course_scse2[i]+"\n"   
                    self.s+="\nRemember to input number only"                 
                    self.sender.sendMessage(self.s)
                    self.count+=1
   

                elif self.year==3:  

                    for i in range (len(self.course_scse3)):
                        self.s+=str(i+1)+":"+self.course_scse3[i]+"\n"
                    self.s+="\nRemember to input number only"
                    self.sender.sendMessage(self.s)
                    self.count+=1


                elif self.year==4:  

                    for i in range (len(self.course_scse4)):
                        self.s+=str(i+1)+":"+self.course_scse4[i]+"\n"
                    self.s+="\nRemember to input number only"
                    self.sender.sendMessage(self.s)
                    self.count+=1


            else:
                self.sender.sendMessage("The input you entered was wrong.\nDont worry you still get to correct yourself")
                self.count=4


        elif self.count==6:

            self.course_study=int(msg['text'])

            if self.teacher_stu=="s":
                self.s1="The course you have problem in: "
            elif self.teacher_stu=="t":                                                #chosing which topic to study/teach according to the year and course chosen before------working
                self.s1="The course you would like to teach: "

            if self.year==1:

                self.s1+=self.course_scse1[self.course_study-1]
                if self.teacher_stu=="s":
                    self.s1+="\n\nSelect topic no you have problem in: \n"
                elif self.teacher_stu=="t":
                    self.s1+="\n\nSelect topic you would like to teach: \n"

                for i in range (len(self.content_scse1[self.course_study-1])):
                    self.s1+=str(i+1)+":"+self.content_scse1[self.course_study-1][i]+"\n"  

            elif self.year==2:

                self.s1+=self.course_scse2[self.course_study-1]
                if self.teacher_stu=="s":
                    self.s1+="\n\nSelect topic no you have problem in: \n"
                elif self.teacher_stu=="t":
                    self.s1+="\n\nSelect topic you would like to teach: \n"

                self.s1+="\nSelect topic no you have problem in: \n"
                for i in range (len(self.content_scse2[self.course_study-1])):
                    self.s1+=str(i+1)+":"+self.content_scse2[self.course_study-1][i]+"\n"     

            elif self.year==3:

                self.s1+=self.course_scse3[self.course_study-1]
                if self.teacher_stu=="s":
                    self.s1+="\n\nSelect topic no you have problem in: \n"
                elif self.teacher_stu=="t":
                    self.s1+="\n\nSelect topic you would like to teach: \n"
                    
                for i in range (len(self.content_scse3[self.course_study-1])):
                    self.s1+=str(i+1)+":"+self.content_scse3[self.course_study-1][i]+"\n"                

            elif self.year==4:

                self.s1+=self.course_scse4[self.course_study-1]
                if self.teacher_stu=="s":
                    self.s1+="\n\nSelect topic no you have problem in: \n"
                elif self.teacher_stu=="t":
                    self.s1+="\n\nSelect topic you would like to teach: \n"
                    
                for i in range (len(self.content_scse4[self.course_study-1])):
                    self.s1+=str(i+1)+":"+self.content_scse4[self.course_study-1][i]+"\n"              

            self.sender.sendMessage(self.s1)
            self.count+=1
            print("course:",self.course_study)

        elif self.count==7:                                         #print the choice you have entered---------working

            self.content_study=int(msg['text'])-1
            if self.teacher_stu=="s":
                if self.year==1:
                    self.content_study=self.content_scse1[self.course_study-1][self.content_study]
                    self.sender.sendMessage("You have problem in:"+self.content_study+"\nIs that right?\nYes\nNo")
                    self.count+=1

                elif self.year==2:
                    self.content_study=self.content_scse2[self.course_study-1][self.content_study]
                    self.sender.sendMessage("You have problem in:"+self.content_study+"\nIs that right?\nYes\nNo")
                    self.count+=1

                elif self.year==3:
                    self.content_study=self.content_scse3[self.course_study-1][self.content_study]
                    self.sender.sendMessage("You have problem in:"+self.content_study+"\nIs that right?\nYes\nNo")
                    self.count+=1

                elif self.year==4:
                    self.content_study=self.content_scse4[self.course_study-1][self.content_study]
                    self.sender.sendMessage("You have problem in:"+self.content_study+"\nIs that right?\nYes\nNo")
                    self.count+=1
                    
                        
            elif self.teacher_stu=="t":
                if self.year==1:
                    self.content_study=self.content_scse1[self.course_study-1][self.content_study]
                    self.sender.sendMessage("You would like to teach: "+self.content_study+"\nIs that right?\nYes\nNo")
                    self.count+=1

                elif self.year==2:
                    self.content_study=self.content_scse2[self.course_study-1][self.content_study]
                    self.sender.sendMessage("You would like to teach: "+self.content_study+"\nIs that right?\nYes\nNo")
                    self.count+=1

                elif self.year==3:
                    self.content_study=self.content_scse3[self.course_study-1][self.content_study]
                    self.sender.sendMessage("You would like to teach: "+self.content_study+"\nIs that right?\nYes\nNo")
                    self.count+=1

                elif self.year==4:
                    self.content_study=self.content_scse4[self.course_study-1][self.content_study]
                    self.sender.sendMessage("You would like to teach: "+self.content_study+"\nIs that right?\nYes\nNo")
                    self.count+=1


        elif self.count==8:
            #creates a folder by seeking your working directory and creating a new file ,specified by our file xtension that can be opened in our python program only (hence all data entered is secured)

            self.yes_no=msg['text']
            if self.yes_no.lower() in ["yes","y"]:
                if not os.path.exists(".\\TuitionBot_Users"):
                    # Making said folder if not found
                    os.mkdir(".\\TuitionBot_Users")
                # Using a generator function to get a list of files in TuitionBot_Users folder
                (root,dir,files) = os.walk(".\\TuitionBot_Users").__next__()
                # Calculating the name of the new file
                filenum = len(files)
                # Opening a new file with .graph extension which is self created but can still be opened in binary mode
                bot_binary = open(".\\TuitionBot_Users\\"+str(filenum+1)+".tuitionBotNTU", "wb")
                # Filling the file with required data
                pickle.dump((self.name,self.teacher_stu,self.year,self.content_study,self.course_study,self.__phone),bot_binary)
                # Remember to close to make sure everything functions smoothly!
                
                #Appending file no and content chosen in list accordingly
                if self.teacher_stu=="s":
                    self.student_list.append([int(filenum+1),self.content_study])
                elif self.teacher_stu=="t":
                    self.teacher_list.append([int(filenum+1),self.content_study])
                bot_binary.close()
                self.sender.sendMessage("We will soon find your match \nPress any key to acknowledge")
                self.count=9
                print("content:",self.content_study)

            else:
                self.sender.sendMessage("You identified that the input you chose were wrong,no worries.You can choose again.")
                self.count=6




        elif self.count==9:

            for i in range (len(self.student_list)):
                for j in range (len(self.teacher_list)):

                    #lenth of list is 2 if no matchong is done already
                    if self.student_list[i][1]==self.teacher_list[j][1] and len(self.teacher_list[j])==2 and len(self.student_list[i])==2 :

                        #extracting data from file created and not from the input of user or previously sored info in the program
                        (root, dir, files) = os.walk(".\\TuitionBot_Users").__next__()
                        files.sort()
                        if self.teacher_stu=="s":
                            match = open(".\\TuitionBot_Users\\" + files[j], "rb")
                            (name1,teacher_stu1,year1,content_study1,course_study,phone1)= pickle.load(match)
                            self.sender.sendMessage("Congratulations :) \nWe have found you a teacher \nYou can contact him/her accordingly \nHis/her details are as follows: \nName:"+name1+"\nPhone Number:"+phone1+"\nPress any key to acknowledge")
                            match.close()

                        elif self.teacher_stu=="t":
                            match = open(".\\TuitionBot_Users\\" + files[i], "rb")
                            (name1,teacher_stu1,year1,content_study1,course_study,phone1)= pickle.load(match)
                            self.sender.sendMessage("Congratulations :) \nWe have found you a student \nYou can contact him/her accordingly \nHis/her details are as follows: \nName:"+name1+"\nPhone Number:"+phone1+"\nPress any key to acknowledge")
                            match.close()

                        self.student_list[i]=self.student_list[i].append("match found")
                        self.teacher_list[i]=self.teacher_list[i].append("match found")
                        ## change nested list to [file no ,content,"match done"]--------length of sub list changes to 3 instead of 2
                        self.match=1

            if self.match==0:
                if self.teacher_stu=="s":
                    self.sender.sendMessage("No teacher available matching with you course content"+"\nPress any key to acknowledge")
                elif self.teacher_stu=="t":
                    self.sender.sendMessage("No student matching with your course content"+"\nPress any key to acknowledge")

            self.count+=1


        
        elif self.count==10:
            print("here10")
            if self.teacher_stu=="s":
                self.str_videos="Meanwhile you can browse through some videos on the topic chosen(We have tried to incoperate as much resources our team could find):"

                if self.year==1:
                    for i in range (len(self.content_scse1[self.course_study-1])):
                        if self.content_study==self.content_scse1[self.course_study-1][i]:
                            if self.year1_videos[self.course_study-1] !="-" and self.year1_videos[self.course_study-1][i] != "-":
                                self.sender.sendMessage(self.str_videos+"\n"+self.year1_videos[self.course_study-1][i])
                if self.year==2:
                    for i in range (len(self.content_scse2[self.course_study-1])):
                        if self.content_study==self.content_scse2[self.course_study-1][i]:
                            if self.year2_videos[self.course_study-1] !="-" and self.year2_videos[self.course_study-1][i] != "-":
                                self.sender.sendMessage(self.str_videos+"\n"+self.year2_videos[self.course_study-1][i])                

                if self.year==3:
                    for i in range (len(self.content_scse3[self.course_study-1])):
                        if self.content_study==self.content_scse3[self.course_study-1][i]:
                            if self.year3_videos[self.course_study-1] !="-" and self.year3_videos[self.course_study-1][i] != "-":
                                self.sender.sendMessage(self.str_videos+"\n"+self.year3_videos[self.course_study-1][i])
                if self.year==4:
                    for i in range (len(self.content_scse4[self.course_study-1])):
                        if self.content_study==self.content_scse4[self.course_study-1][i]:
                            if self.year4_videos[self.course_study-1] !="-" and self.year4_videos[self.course_study-1][i] != "-":
                                self.sender.sendMessage(self.str_videos+"\n"+self.year4_videos[self.course_study-1][i])

            self.sender.sendMessage("Thank You for choosing TuitionBot NTU")
            self.count=0

        #admin functions
        elif self.count==11:

            self.password=msg['text']
            if self.password==self.__password:

                self.sender.sendMessage("Enter file number you want to read\nCurrent number of files:"+str(self.current_no_of_files))
                self.count+=1

            else:
                self.sender.sendMessage("You are not smart enough man ,dont try to be  ;)")
                self.count=0
          
        elif self.count==12:
            self.file_no=msg['text']
            # Getting the filelist
            (root, dir, files) = os.walk(".\\TuitionBot_Users").__next__()
            # Sorting so as to be able to determine the last file
            files.sort()
            # Opening the file
            previous = open(".\\TuitionBot_Users\\" + files[int(self.file_no)-1], "rb")
            # Getting the critical variables required to make graph
            (name,teacher_stu,year,content_study,course_study,phone)= pickle.load(previous)
            school="SCSE"
            self.str_admin="Name: "+str(name)+"\nTeacher/Student: "+str(teacher_stu.upper())+"\nYear chosen: "+str(year)+"\nSchool chosen: "+"SCSE"+"\nContent Chosen: "+str(content_study)+"\nPhone Number: "+phone

            self.sender.sendMessage(self.str_admin)
            # Closing to ensure smooth functioning
            previous.close()
            self.count=0


TOKEN = "299269480:AAGS9ocoWp0k1z_zqWp86P4Ixo5tUqcjH08"   # add token once new bot made

bot = telepot.DelegatorBot(TOKEN, [
pave_event_space()(
        per_chat_id(), create_open, MessageCounter,timeout=10000000),
])
bot.message_loop(run_forever='Listening ...')
