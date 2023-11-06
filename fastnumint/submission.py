"""This is what I submitted for the class, because it was fastest based on my testing"""

from heapq import heappop, heappush  # ever so slightly faster than bisect.insort and list.pop

gk_roots = {
    # kronrod_degree: [
    #     (x, kronrod_weight, gauss_weight),
    #     ...
    # ],
    # ...
    15: [
        (0.000000000000000000000000000000000e+00, 2.094821410847278280129991748917143e-01,
         4.179591836734693877551020408163265e-01),
        (+2.077849550078984676006894037732449e-01, 2.044329400752988924141619992346491e-01, 0),
        (+4.058451513773971669066064120769615e-01, 1.903505780647854099132564024210137e-01,
         3.818300505051189449503697754889751e-01),
        (+5.860872354676911302941448382587296e-01, 1.690047266392679028265834265985503e-01, 0),
        (+7.415311855993944398638647732807884e-01, 1.406532597155259187451895905102379e-01,
         2.797053914892766679014677714237796e-01),
        (+8.648644233597690727897127886409262e-01, 1.047900103222501838398763225415180e-01, 0),
        (+9.491079123427585245261896840478513e-01, 6.309209262997855329070066318920429e-02,
         1.294849661688696932706114326790820e-01),
        (+9.914553711208126392068546975263285e-01, 2.293532201052922496373200805896959e-02, 0),
        (-2.077849550078984676006894037732449e-01, 2.044329400752988924141619992346491e-01, 0),
        (-4.058451513773971669066064120769615e-01, 1.903505780647854099132564024210137e-01,
         3.818300505051189449503697754889751e-01),
        (-5.860872354676911302941448382587296e-01, 1.690047266392679028265834265985503e-01, 0),
        (-7.415311855993944398638647732807884e-01, 1.406532597155259187451895905102379e-01,
         2.797053914892766679014677714237796e-01),
        (-8.648644233597690727897127886409262e-01, 1.047900103222501838398763225415180e-01, 0),
        (-9.491079123427585245261896840478513e-01, 6.309209262997855329070066318920429e-02,
         1.294849661688696932706114326790820e-01),
        (-9.914553711208126392068546975263285e-01, 2.293532201052922496373200805896959e-02, 0),
    ],
    21: [
        (0.000000000000000000000000000000000e+00, 1.494455540029169056649364683898212e-01, 0),
        (+1.488743389816312108848260011297200e-01, 1.477391049013384913748415159720680e-01,
         2.955242247147528701738929946513383e-01),
        (+2.943928627014601981311266031038656e-01, 1.427759385770600807970942731387171e-01, 0),
        (+4.333953941292471907992659431657842e-01, 1.347092173114733259280540017717068e-01,
         2.692667193099963550912269215694694e-01),
        (+5.627571346686046833390000992726941e-01, 1.234919762620658510779581098310742e-01, 0),
        (+6.794095682990244062343273651148736e-01, 1.093871588022976418992105903258050e-01,
         2.190863625159820439955349342281632e-01),
        (+7.808177265864168970637175783450424e-01, 9.312545458369760553506546508336634e-02, 0),
        (+8.650633666889845107320966884234930e-01, 7.503967481091995276704314091619001e-02,
         1.494513491505805931457763396576973e-01),
        (+9.301574913557082260012071800595083e-01, 5.475589657435199603138130024458018e-02, 0),
        (+9.739065285171717200779640120844521e-01, 3.255816230796472747881897245938976e-02,
         6.667134430868813759356880989333179e-02),
        (+9.956571630258080807355272806890028e-01, 1.169463886737187427806439606219205e-02, 0),
        (-1.488743389816312108848260011297200e-01, 1.477391049013384913748415159720680e-01,
         2.955242247147528701738929946513383e-01),
        (-2.943928627014601981311266031038656e-01, 1.427759385770600807970942731387171e-01, 0),
        (-4.333953941292471907992659431657842e-01, 1.347092173114733259280540017717068e-01,
         2.692667193099963550912269215694694e-01),
        (-5.627571346686046833390000992726941e-01, 1.234919762620658510779581098310742e-01, 0),
        (-6.794095682990244062343273651148736e-01, 1.093871588022976418992105903258050e-01,
         2.190863625159820439955349342281632e-01),
        (-7.808177265864168970637175783450424e-01, 9.312545458369760553506546508336634e-02, 0),
        (-8.650633666889845107320966884234930e-01, 7.503967481091995276704314091619001e-02,
         1.494513491505805931457763396576973e-01),
        (-9.301574913557082260012071800595083e-01, 5.475589657435199603138130024458018e-02, 0),
        (-9.739065285171717200779640120844521e-01, 3.255816230796472747881897245938976e-02,
         6.667134430868813759356880989333179e-02),
        (-9.956571630258080807355272806890028e-01, 1.169463886737187427806439606219205e-02, 0),
    ],
    31: [
        (0.000000000000000000000000000000000e+00, 1.013300070147915490173747927674925e-01,
         2.025782419255612728806201999675193e-01),
        (+1.011420669187174990270742314473923e-01, 1.007698455238755950449466626175697e-01, 0),
        (+2.011940939974345223006283033945962e-01, 9.917359872179195933239317348460313e-02,
         1.984314853271115764561183264438393e-01),
        (+2.991800071531688121667800242663890e-01, 9.664272698362367850517990762758934e-02, 0),
        (+3.941513470775633698972073709810455e-01, 9.312659817082532122548687274734572e-02,
         1.861610000155622110268005618664228e-01),
        (+4.850818636402396806936557402323506e-01, 8.856444305621177064727544369377430e-02, 0),
        (+5.709721726085388475372267372539106e-01, 8.308050282313302103828924728610379e-02,
         1.662692058169939335532008604812088e-01),
        (+6.509967412974169705337358953132747e-01, 7.684968075772037889443277748265901e-02, 0),
        (+7.244177313601700474161860546139380e-01, 6.985412131872825870952007709914748e-02,
         1.395706779261543144478047945110283e-01),
        (+7.904185014424659329676492948179473e-01, 6.200956780067064028513923096080293e-02, 0),
        (+8.482065834104272162006483207742169e-01, 5.348152469092808726534314723943030e-02,
         1.071592204671719350118695466858693e-01),
        (+8.972645323440819008825096564544959e-01, 4.458975132476487660822729937327969e-02, 0),
        (+9.372733924007059043077589477102095e-01, 3.534636079137584622203794847836005e-02,
         7.036604748810812470926741645066734e-02),
        (+9.677390756791391342573479787843372e-01, 2.546084732671532018687400101965336e-02, 0),
        (+9.879925180204854284895657185866126e-01, 1.500794732931612253837476307580727e-02,
         3.075324199611726835462839357720442e-02),
        (+9.980022986933970602851728401522712e-01, 5.377479872923348987792051430127650e-03, 0),
        (-1.011420669187174990270742314473923e-01, 1.007698455238755950449466626175697e-01, 0),
        (-2.011940939974345223006283033945962e-01, 9.917359872179195933239317348460313e-02,
         1.984314853271115764561183264438393e-01),
        (-2.991800071531688121667800242663890e-01, 9.664272698362367850517990762758934e-02, 0),
        (-3.941513470775633698972073709810455e-01, 9.312659817082532122548687274734572e-02,
         1.861610000155622110268005618664228e-01),
        (-4.850818636402396806936557402323506e-01, 8.856444305621177064727544369377430e-02, 0),
        (-5.709721726085388475372267372539106e-01, 8.308050282313302103828924728610379e-02,
         1.662692058169939335532008604812088e-01),
        (-6.509967412974169705337358953132747e-01, 7.684968075772037889443277748265901e-02, 0),
        (-7.244177313601700474161860546139380e-01, 6.985412131872825870952007709914748e-02,
         1.395706779261543144478047945110283e-01),
        (-7.904185014424659329676492948179473e-01, 6.200956780067064028513923096080293e-02, 0),
        (-8.482065834104272162006483207742169e-01, 5.348152469092808726534314723943030e-02,
         1.071592204671719350118695466858693e-01),
        (-8.972645323440819008825096564544959e-01, 4.458975132476487660822729937327969e-02, 0),
        (-9.372733924007059043077589477102095e-01, 3.534636079137584622203794847836005e-02,
         7.036604748810812470926741645066734e-02),
        (-9.677390756791391342573479787843372e-01, 2.546084732671532018687400101965336e-02, 0),
        (-9.879925180204854284895657185866126e-01, 1.500794732931612253837476307580727e-02,
         3.075324199611726835462839357720442e-02),
        (-9.980022986933970602851728401522712e-01, 5.377479872923348987792051430127650e-03, 0),
    ],
    41: [
        (0.000000000000000000000000000000000e+00, 7.660071191799965644504990153010174e-02, 0),
        (+7.652652113349733375464040939883821e-02, 7.637786767208073670550283503806100e-02,
         1.527533871307258506980843319550976e-01),
        (+1.526054652409226755052202410226775e-01, 7.570449768455667465954277537661656e-02, 0),
        (+2.277858511416450780804961953685746e-01, 7.458287540049918898658141836248753e-02,
         1.491729864726037467878287370019694e-01),
        (+3.016278681149130043205553568585923e-01, 7.303069033278666749518941765891311e-02, 0),
        (+3.737060887154195606725481770249272e-01, 7.105442355344406830579036172321017e-02,
         1.420961093183820513292983250671649e-01),
        (+4.435931752387251031999922134926401e-01, 6.864867292852161934562341188536780e-02, 0),
        (+5.108670019508270980043640509552510e-01, 6.583459713361842211156355696939794e-02,
         1.316886384491766268984944997481631e-01),
        (+5.751404468197103153429460365864251e-01, 6.265323755478116802587012217425498e-02, 0),
        (+6.360536807265150254528366962262859e-01, 5.911140088063957237496722064859422e-02,
         1.181945319615184173123773777113823e-01),
        (+6.932376563347513848054907118459315e-01, 5.519510534828599474483237241977733e-02, 0),
        (+7.463319064601507926143050703556416e-01, 5.094457392372869193270767005034495e-02,
         1.019301198172404350367501354803499e-01),
        (+7.950414288375511983506388332727879e-01, 4.643482186749767472023188092610752e-02, 0),
        (+8.391169718222188233945290617015207e-01, 4.166887332797368626378830593689474e-02,
         8.327674157670474872475814322204621e-02),
        (+8.782768112522819760774429951130785e-01, 3.660016975820079803055724070721101e-02, 0),
        (+9.122344282513259058677524412032981e-01, 3.128730677703279895854311932380074e-02,
         6.267204833410906356950653518704161e-02),
        (+9.408226338317547535199827222124434e-01, 2.588213360495115883450506709615314e-02, 0),
        (+9.639719272779137912676661311972772e-01, 2.038837346126652359801023143275471e-02,
         4.060142980038694133103995227493211e-02),
        (+9.815078774502502591933429947202169e-01, 1.462616925697125298378796030886836e-02, 0),
        (+9.931285991850949247861223884713203e-01, 8.600269855642942198661787950102347e-03,
         1.761400713915211831186196235185282e-02),
        (+9.988590315882776638383155765458630e-01, 3.073583718520531501218293246030987e-03, 0),
        (-7.652652113349733375464040939883821e-02, 7.637786767208073670550283503806100e-02,
         1.527533871307258506980843319550976e-01),
        (-1.526054652409226755052202410226775e-01, 7.570449768455667465954277537661656e-02, 0),
        (-2.277858511416450780804961953685746e-01, 7.458287540049918898658141836248753e-02,
         1.491729864726037467878287370019694e-01),
        (-3.016278681149130043205553568585923e-01, 7.303069033278666749518941765891311e-02, 0),
        (-3.737060887154195606725481770249272e-01, 7.105442355344406830579036172321017e-02,
         1.420961093183820513292983250671649e-01),
        (-4.435931752387251031999922134926401e-01, 6.864867292852161934562341188536780e-02, 0),
        (-5.108670019508270980043640509552510e-01, 6.583459713361842211156355696939794e-02,
         1.316886384491766268984944997481631e-01),
        (-5.751404468197103153429460365864251e-01, 6.265323755478116802587012217425498e-02, 0),
        (-6.360536807265150254528366962262859e-01, 5.911140088063957237496722064859422e-02,
         1.181945319615184173123773777113823e-01),
        (-6.932376563347513848054907118459315e-01, 5.519510534828599474483237241977733e-02, 0),
        (-7.463319064601507926143050703556416e-01, 5.094457392372869193270767005034495e-02,
         1.019301198172404350367501354803499e-01),
        (-7.950414288375511983506388332727879e-01, 4.643482186749767472023188092610752e-02, 0),
        (-8.391169718222188233945290617015207e-01, 4.166887332797368626378830593689474e-02,
         8.327674157670474872475814322204621e-02),
        (-8.782768112522819760774429951130785e-01, 3.660016975820079803055724070721101e-02, 0),
        (-9.122344282513259058677524412032981e-01, 3.128730677703279895854311932380074e-02,
         6.267204833410906356950653518704161e-02),
        (-9.408226338317547535199827222124434e-01, 2.588213360495115883450506709615314e-02, 0),
        (-9.639719272779137912676661311972772e-01, 2.038837346126652359801023143275471e-02,
         4.060142980038694133103995227493211e-02),
        (-9.815078774502502591933429947202169e-01, 1.462616925697125298378796030886836e-02, 0),
        (-9.931285991850949247861223884713203e-01, 8.600269855642942198661787950102347e-03,
         1.761400713915211831186196235185282e-02),
        (-9.988590315882776638383155765458630e-01, 3.073583718520531501218293246030987e-03, 0),
    ],
    51: [
        (0.000000000000000000000000000000000e+00, 6.158081806783293507875982424006455e-02,
         1.231760537267154512039028730790501e-01),
        (+6.154448300568507888654639236679663e-02, 6.147118987142531666154413196526418e-02, 0),
        (+1.228646926107103963873598188080368e-01, 6.112850971705304830585903041629271e-02,
         1.222424429903100416889595189458515e-01),
        (+1.837189394210488920159698887595284e-01, 6.053945537604586294536026751756543e-02, 0),
        (+2.438668837209884320451903627974516e-01, 5.972034032417405997909929193256185e-02,
         1.194557635357847722281781265129010e-01),
        (+3.030895389311078301674789099803393e-01, 5.868968002239420796197417585678776e-02, 0),
        (+3.611723058093878377358217301276407e-01, 5.743711636156783285358269393950647e-02,
         1.148582591457116483393255458695558e-01),
        (+4.178853821930377488518143945945725e-01, 5.595081122041231730824068638274735e-02, 0),
        (+4.730027314457149605221821150091920e-01, 5.425112988854549014454337045987561e-02,
         1.085196244742636531160939570501166e-01),
        (+5.263252843347191825996237781580102e-01, 5.236288580640747586436671213787271e-02, 0),
        (+5.776629302412229677236898416126541e-01, 5.027767908071567196332525943344008e-02,
         1.005359490670506442022068903926858e-01),
        (+6.268100990103174127881226816245179e-01, 4.798253713883671390639225575691475e-02, 0),
        (+6.735663684734683644851206332476222e-01, 4.550291304992178890987058475266039e-02,
         9.102826198296364981149722070289165e-02),
        (+7.177664068130843881866540797732978e-01, 4.287284502017004947689579243949516e-02, 0),
        (+7.592592630373576305772828652043610e-01, 4.008382550403238207483928446707565e-02,
         8.014070033500101801323495966911130e-02),
        (+7.978737979985000594104109049943066e-01, 3.711627148341554356033062536761988e-02, 0),
        (+8.334426287608340014210211086935696e-01, 3.400213027432933783674879522955120e-02,
         6.803833381235691720718718565670797e-02),
        (+8.658470652932755954489969695883401e-01, 3.079230016738748889110902021522859e-02, 0),
        (+8.949919978782753688510420067828050e-01, 2.747531758785173780294845551781108e-02,
         5.490469597583519192593689154047332e-02),
        (+9.207471152817015617463460845463306e-01, 2.400994560695321622009248916488108e-02, 0),
        (+9.429745712289743394140111696584705e-01, 2.043537114588283545656829223593897e-02,
         4.093915670130631265562348771164595e-02),
        (+9.616149864258425124181300336601672e-01, 1.684781770912829823151666753633632e-02, 0),
        (+9.766639214595175114983153864795941e-01, 1.323622919557167481365640584697624e-02,
         2.635498661503213726190181529529914e-02),
        (+9.880357945340772476373310145774062e-01, 9.473973386174151607207710523655324e-03, 0),
        (+9.955569697904980979087849468939016e-01, 5.561932135356713758040236901065522e-03,
         1.139379850102628794790296411323477e-02),
        (+9.992621049926098341934574865403406e-01, 1.987383892330315926507851882843410e-03, 0),
        (-6.154448300568507888654639236679663e-02, 6.147118987142531666154413196526418e-02, 0),
        (-1.228646926107103963873598188080368e-01, 6.112850971705304830585903041629271e-02,
         1.222424429903100416889595189458515e-01),
        (-1.837189394210488920159698887595284e-01, 6.053945537604586294536026751756543e-02, 0),
        (-2.438668837209884320451903627974516e-01, 5.972034032417405997909929193256185e-02,
         1.194557635357847722281781265129010e-01),
        (-3.030895389311078301674789099803393e-01, 5.868968002239420796197417585678776e-02, 0),
        (-3.611723058093878377358217301276407e-01, 5.743711636156783285358269393950647e-02,
         1.148582591457116483393255458695558e-01),
        (-4.178853821930377488518143945945725e-01, 5.595081122041231730824068638274735e-02, 0),
        (-4.730027314457149605221821150091920e-01, 5.425112988854549014454337045987561e-02,
         1.085196244742636531160939570501166e-01),
        (-5.263252843347191825996237781580102e-01, 5.236288580640747586436671213787271e-02, 0),
        (-5.776629302412229677236898416126541e-01, 5.027767908071567196332525943344008e-02,
         1.005359490670506442022068903926858e-01),
        (-6.268100990103174127881226816245179e-01, 4.798253713883671390639225575691475e-02, 0),
        (-6.735663684734683644851206332476222e-01, 4.550291304992178890987058475266039e-02,
         9.102826198296364981149722070289165e-02),
        (-7.177664068130843881866540797732978e-01, 4.287284502017004947689579243949516e-02, 0),
        (-7.592592630373576305772828652043610e-01, 4.008382550403238207483928446707565e-02,
         8.014070033500101801323495966911130e-02),
        (-7.978737979985000594104109049943066e-01, 3.711627148341554356033062536761988e-02, 0),
        (-8.334426287608340014210211086935696e-01, 3.400213027432933783674879522955120e-02,
         6.803833381235691720718718565670797e-02),
        (-8.658470652932755954489969695883401e-01, 3.079230016738748889110902021522859e-02, 0),
        (-8.949919978782753688510420067828050e-01, 2.747531758785173780294845551781108e-02,
         5.490469597583519192593689154047332e-02),
        (-9.207471152817015617463460845463306e-01, 2.400994560695321622009248916488108e-02, 0),
        (-9.429745712289743394140111696584705e-01, 2.043537114588283545656829223593897e-02,
         4.093915670130631265562348771164595e-02),
        (-9.616149864258425124181300336601672e-01, 1.684781770912829823151666753633632e-02, 0),
        (-9.766639214595175114983153864795941e-01, 1.323622919557167481365640584697624e-02,
         2.635498661503213726190181529529914e-02),
        (-9.880357945340772476373310145774062e-01, 9.473973386174151607207710523655324e-03, 0),
        (-9.955569697904980979087849468939016e-01, 5.561932135356713758040236901065522e-03,
         1.139379850102628794790296411323477e-02),
        (-9.992621049926098341934574865403406e-01, 1.987383892330315926507851882843410e-03, 0),
    ],
    61: [
        (0.000000000000000000000000000000000e+00, 5.149472942945156755834043364709931e-02, 0),
        (+5.147184255531769583302521316672257e-02, 5.142612853745902593386287921578126e-02,
         1.028526528935588403412856367054150e-01),
        (+1.028069379667370301470967513180006e-01, 5.122154784925877217065628260494421e-02, 0),
        (+1.538699136085835469637946727432559e-01, 5.088179589874960649229747304980469e-02,
         1.017623897484055045964289521685540e-01),
        (+2.045251166823098914389576710020247e-01, 5.040592140278234684089308565358503e-02, 0),
        (+2.546369261678898464398051298178051e-01, 4.979568342707420635781156937994233e-02,
         9.959342058679526706278028210356948e-02),
        (+3.040732022736250773726771071992566e-01, 4.905543455502977888752816536723817e-02, 0),
        (+3.527047255308781134710372070893739e-01, 4.818586175708712914077949229830459e-02,
         9.636873717464425963946862635180987e-02),
        (+4.004012548303943925354762115426606e-01, 4.718554656929915394526147818109949e-02, 0),
        (+4.470337695380891767806099003228540e-01, 4.605923827100698811627173555937358e-02,
         9.212252223778612871763270708761877e-02),
        (+4.924804678617785749936930612077088e-01, 4.481480013316266319235555161672324e-02, 0),
        (+5.366241481420198992641697933110728e-01, 4.345253970135606931683172811707326e-02,
         8.689978720108297980238753071512570e-02),
        (+5.793452358263616917560249321725405e-01, 4.196981021516424614714754128596976e-02, 0),
        (+6.205261829892428611404775564311893e-01, 4.037453895153595911199527975246811e-02,
         8.075589522942021535469493846052973e-02),
        (+6.600610641266269613700536681492708e-01, 3.867894562472759295034865153228105e-02, 0),
        (+6.978504947933157969322923880266401e-01, 3.688236465182122922391106561713597e-02,
         7.375597473770520626824385002219073e-02),
        (+7.337900624532268047261711313695276e-01, 3.497933802806002413749967073146788e-02, 0),
        (+7.677774321048261949179773409745031e-01, 3.298144705748372603181419101685393e-02,
         6.597422988218049512812851511596236e-02),
        (+7.997278358218390830136689423226832e-01, 3.090725756238776247288425294309227e-02, 0),
        (+8.295657623827683974428981197325019e-01, 2.875404876504129284397878535433421e-02,
         5.749315621761906648172168940205613e-02),
        (+8.572052335460610989586585106589439e-01, 2.650995488233310161060170933507541e-02, 0),
        (+8.825605357920526815431164625302256e-01, 2.419116207808060136568637072523203e-02,
         4.840267283059405290293814042280752e-02),
        (+9.055733076999077985465225589259583e-01, 2.182803582160919229716748573833899e-02, 0),
        (+9.262000474292743258793242770804740e-01, 1.941414119394238117340895105012846e-02,
         3.879919256962704959680193644634769e-02),
        (+9.443744447485599794158313240374391e-01, 1.692088918905327262757228942032209e-02, 0),
        (+9.600218649683075122168710255817977e-01, 1.436972950704580481245143244358001e-02,
         2.878470788332336934971917961129204e-02),
        (+9.731163225011262683746938684237069e-01, 1.182301525349634174223289885325059e-02, 0),
        (+9.836681232797472099700325816056628e-01, 9.273279659517763428441146892024360e-03,
         1.846646831109095914230213191204727e-02),
        (+9.916309968704045948586283661094857e-01, 6.630703915931292173319826369750168e-03, 0),
        (+9.968934840746495402716300509186953e-01, 3.890461127099884051267201844515503e-03,
         7.968192496166605615465883474673622e-03),
        (+9.994844100504906375713258957058108e-01, 1.389013698677007624551591226759700e-03, 0),
        (-5.147184255531769583302521316672257e-02, 5.142612853745902593386287921578126e-02,
         1.028526528935588403412856367054150e-01),
        (-1.028069379667370301470967513180006e-01, 5.122154784925877217065628260494421e-02, 0),
        (-1.538699136085835469637946727432559e-01, 5.088179589874960649229747304980469e-02,
         1.017623897484055045964289521685540e-01),
        (-2.045251166823098914389576710020247e-01, 5.040592140278234684089308565358503e-02, 0),
        (-2.546369261678898464398051298178051e-01, 4.979568342707420635781156937994233e-02,
         9.959342058679526706278028210356948e-02),
        (-3.040732022736250773726771071992566e-01, 4.905543455502977888752816536723817e-02, 0),
        (-3.527047255308781134710372070893739e-01, 4.818586175708712914077949229830459e-02,
         9.636873717464425963946862635180987e-02),
        (-4.004012548303943925354762115426606e-01, 4.718554656929915394526147818109949e-02, 0),
        (-4.470337695380891767806099003228540e-01, 4.605923827100698811627173555937358e-02,
         9.212252223778612871763270708761877e-02),
        (-4.924804678617785749936930612077088e-01, 4.481480013316266319235555161672324e-02, 0),
        (-5.366241481420198992641697933110728e-01, 4.345253970135606931683172811707326e-02,
         8.689978720108297980238753071512570e-02),
        (-5.793452358263616917560249321725405e-01, 4.196981021516424614714754128596976e-02, 0),
        (-6.205261829892428611404775564311893e-01, 4.037453895153595911199527975246811e-02,
         8.075589522942021535469493846052973e-02),
        (-6.600610641266269613700536681492708e-01, 3.867894562472759295034865153228105e-02, 0),
        (-6.978504947933157969322923880266401e-01, 3.688236465182122922391106561713597e-02,
         7.375597473770520626824385002219073e-02),
        (-7.337900624532268047261711313695276e-01, 3.497933802806002413749967073146788e-02, 0),
        (-7.677774321048261949179773409745031e-01, 3.298144705748372603181419101685393e-02,
         6.597422988218049512812851511596236e-02),
        (-7.997278358218390830136689423226832e-01, 3.090725756238776247288425294309227e-02, 0),
        (-8.295657623827683974428981197325019e-01, 2.875404876504129284397878535433421e-02,
         5.749315621761906648172168940205613e-02),
        (-8.572052335460610989586585106589439e-01, 2.650995488233310161060170933507541e-02, 0),
        (-8.825605357920526815431164625302256e-01, 2.419116207808060136568637072523203e-02,
         4.840267283059405290293814042280752e-02),
        (-9.055733076999077985465225589259583e-01, 2.182803582160919229716748573833899e-02, 0),
        (-9.262000474292743258793242770804740e-01, 1.941414119394238117340895105012846e-02,
         3.879919256962704959680193644634769e-02),
        (-9.443744447485599794158313240374391e-01, 1.692088918905327262757228942032209e-02, 0),
        (-9.600218649683075122168710255817977e-01, 1.436972950704580481245143244358001e-02,
         2.878470788332336934971917961129204e-02),
        (-9.731163225011262683746938684237069e-01, 1.182301525349634174223289885325059e-02, 0),
        (-9.836681232797472099700325816056628e-01, 9.273279659517763428441146892024360e-03,
         1.846646831109095914230213191204727e-02),
        (-9.916309968704045948586283661094857e-01, 6.630703915931292173319826369750168e-03, 0),
        (-9.968934840746495402716300509186953e-01, 3.890461127099884051267201844515503e-03,
         7.968192496166605615465883474673622e-03),
        (-9.994844100504906375713258957058108e-01, 1.389013698677007624551591226759700e-03, 0),
    ],
}

num_points = 21
_roots = gk_roots[num_points]
by_integral = lambda seg: seg[1]
by_error = lambda seg: seg[0]


def print_nonconvergence_warning():
    print('----------------------------------')
    print('   WARNING: maxiter was reached   ')
    print('Your calculation did not converge!')
    print('----------------------------------')
    print()


def gauss_kronrod(f, a, b):
    scaling = (b - a) / 2
    midpoint = (a + b) / 2
    nodes = [f(scaling * x + midpoint) for x, _, _ in _roots]
    gauss = sum(fx * wg for fx, (_, _, wg) in zip(nodes, _roots) if wg) * scaling
    kronrod = sum(fx * wk for fx, (_, wk, _) in zip(nodes, _roots)) * scaling
    return -abs(kronrod - gauss), kronrod  # this format enables heapq compatibility


def int_num(f, a, b, tol=1e-4, maxiter=1000):
    segments = [(*gauss_kronrod(f, a, b), a, b)]
    for i in range(maxiter):
        if -sum(map(by_error, segments)) <= tol:
            return sum(map(by_integral, segments))

        # bisect the segment with the largest error
        _, _, a, b = heappop(segments)
        m = (a + b) / 2
        heappush(segments, (*gauss_kronrod(f, a, m), a, m))
        heappush(segments, (*gauss_kronrod(f, m, b), m, b))

    if -sum(map(by_error, segments)) > tol:
        print_nonconvergence_warning()
    return sum(map(by_integral, segments))
