import re
import json


text = """
<script>
      window.__NUXT__ = (function(a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, A, B, C, D, E) {
        r.id = 1055467;
        r.type = "shop";
        r.username = "NedimAuto";
        r.avatar = "http:\u002F\u002Fs8.pik.ba\u002Favatari\u002Favatar-1055467-08f812000f.jpg";
        r.medals = [{
          type: "years",
          text: "Medalja za više od 8 godine na OLX.ba",
          value: 8,
          url: "https:\u002F\u002Fd4n0y8dshd77z.cloudfront.net\u002Fassets\u002Fmedals\u002Fduze_od_8.png"
        }, {
          type: "verification",
          text: "Korisnik je verifikovao telefon i email",
          url: "https:\u002F\u002Fd4n0y8dshd77z.cloudfront.net\u002Fassets\u002Fmedals\u002Fverifikovan_broj_ili_email.png"
        }, {
          type: "address",
          text: "Korisnik je verifikovao svoju poštansku adresu",
          url: "https:\u002F\u002Fd4n0y8dshd77z.cloudfront.net\u002Fassets\u002Fmedals\u002Fverifikovana_adresa.png"
        }];
        r.delivery_enabled = f;
        r.settings = {
          privacy: {
            allow_comments: f,
            allow_view_phone: f,
            allow_private_messages: f
          }
        };
        r.avg_response_time = 1087951;
        r.phone = "38762644655";
        r.location = {
          id: s,
          name: t,
          location: {
            lat: u,
            lon: v
          },
          canton_id: j
        };
        return {
          layout: "default",
          data: [{
            title: q,
            listing: {
              id: 51829903,
              type: "single",
              title: q,
              slug: "vw-tiguan-4motion-20-tdi-2012-god",
              short_description: "Extra stanje,Tek uvezen,Može zamjena za jeftinije ",
              additional: {
                description: "\u003Cdiv\u003E\u003Cb\u003EVW TIGUAN 4MOTION \u003Cbr\u003E\n\u003C\u002Fb\u003E\u003C\u002Fdiv\u003E\u003Cdiv\u003E\u003Cb\u003E2012 godina \u003Cbr\u003E\n\u003C\u002Fb\u003E\u003C\u002Fdiv\u003E\u003Cdiv\u003E\u003Cb\u003E2.0 TDI 103 kW Euro5 \u003Cbr\u003E\n\u003C\u002Fb\u003E\u003C\u002Fdiv\u003E\u003Cdiv\u003E\u003Cb\u003EManuelni mjenjač \u003Cbr\u003E\n\u003C\u002Fb\u003E\u003C\u002Fdiv\u003E\u003Cdiv\u003E\u003Cb\u003E231000 prešao \u003Cbr\u003E\n\u003C\u002Fb\u003E\u003C\u002Fdiv\u003E\u003Cdiv\u003E\u003Cb\u003EServisna knjiga \u003Cbr\u003E\n\u003C\u002Fb\u003E\u003C\u002Fdiv\u003E\u003Cdiv\u003E\u003Cb\u003E2 ključa \u003Cbr\u003E\n\u003C\u002Fb\u003E\u003C\u002Fdiv\u003E\u003Cdiv\u003E\u003Cb\u003ENa zadnjoj slici imate broj šasije za provjeru \u003Cbr\u003E\n\u003C\u002Fb\u003E\u003C\u002Fdiv\u003E\u003Cdiv\u003E\u003Cb\u003ETek uvezen plaćeno sve do registracije \u003Cbr\u003E\n\u003C\u002Fb\u003E\u003C\u002Fdiv\u003E\u003Cdiv\u003E\u003Cb\u003EPapiri uredni prevod odmah \u003Cbr\u003E\n\u003C\u002Fb\u003E\u003C\u002Fdiv\u003E\u003Cdiv\u003E\u003Cb\u003EFULL OPREMA!\u003Cbr\u003E\n\u003C\u002Fb\u003E\u003C\u002Fdiv\u003E\u003Cdiv\u003E\u003Cb\u003EAutomobil odlično očuvan \u003Cbr\u003E\n\u003C\u002Fb\u003E\u003C\u002Fdiv\u003E\u003Cdiv\u003E\u003Cb\u003EKupovina vozila isključivo uz obaveznu probnu vožnju \u003Cbr\u003E\n\u003C\u002Fb\u003E\u003C\u002Fdiv\u003E\u003Cdiv\u003E\u003Cb\u003EMožete dovesti svog majstora da pregleda ispravnost vozila \u003Cbr\u003E\n\u003C\u002Fb\u003E\u003C\u002Fdiv\u003E\u003Cdiv\u003E\u003Cb\u003EMogućnost dovoza na kućnu adresu ili vađenje probnih tablica \u003Cbr\u003E\n\u003C\u002Fb\u003E\u003C\u002Fdiv\u003E\u003Cdiv\u003E\u003Cb\u003EKontakt broj 062 644 655 \u003Cbr\u003E\n\u003C\u002Fb\u003E\u003C\u002Fdiv\u003E\u003Cdiv\u003E\u003Cb\u003EPOGLEDAJTE I OSTALU PONUDU NA PROFILU \u003C\u002Fb\u003E\u003C\u002Fdiv\u003E",
                created_at: 1676434840,
                updated_at: 1676792852
              },
              user: r,
              price: 24999,
              regular_price: h,
              price_history: [],
              listing_type: "sell",
              price_by_agreement: a,
              visible: f,
              quantity: g,
              feedbacks: h,
              questions: h,
              status: "active",
              available: a,
              state: w,
              shipping: "no_shipping",
              shipping_available: a,
              free_delivery: a,
              sponsored: i,
              highlighted: e,
              urgent: e,
              exchange_for: e,
              attributes: [{
                id: x,
                type: b,
                value: "4\u002F5",
                name: "Broj vrata"
              }, {
                id: 59,
                type: b,
                value: "Terenac",
                name: "Tip"
              }, {
                id: y,
                type: b,
                value: "Dizel",
                name: "Gorivo"
              }, {
                id: i,
                type: k,
                value: 2012,
                name: "Godište"
              }, {
                id: l,
                type: k,
                value: 231000,
                name: "Kilometraža"
              }, {
                id: j,
                type: k,
                value: 140,
                name: "Konjskih snaga"
              }, {
                id: z,
                type: k,
                value: i,
                name: "Kubikaža"
              }, {
                id: 5,
                type: k,
                value: 103,
                name: "Kilovata (KW)"
              }, {
                id: 2052,
                type: b,
                value: "Sva četiri",
                name: "Pogon"
              }, {
                id: 4640,
                type: b,
                value: c,
                name: "Turbo"
              }, {
                id: 2475,
                type: b,
                value: "Euro 5",
                name: "Emisioni standard"
              }, {
                id: 1171,
                type: b,
                value: "17",
                name: "Veličina felgi"
              }, {
                id: 52,
                type: b,
                value: "Manuelni",
                name: "Transmisija"
              }, {
                id: 2435,
                type: b,
                value: "6+R",
                name: "Broj stepeni prijenosa"
              }, {
                id: 62,
                type: b,
                value: "Siva",
                name: "Boja"
              }, {
                id: 1835,
                type: b,
                value: "Nazad",
                name: "Parking senzori"
              }, {
                id: 5242,
                type: b,
                value: c,
                name: "Park assist"
              }, {
                id: 57,
                type: b,
                value: "DVD-MP3 plus LCD display",
                name: "Muzika\u002Fozvučenje"
              }, {
                id: 903,
                type: b,
                value: c,
                name: "Metalik"
              }, {
                id: 2423,
                type: b,
                value: "2013",
                name: "Godina prve registracije"
              }, {
                id: 2056,
                type: b,
                value: c,
                name: "Ocarinjen"
              }, {
                id: 5011,
                type: b,
                value: "Ljetne",
                name: "Posjeduje gume"
              }, {
                id: 4734,
                type: b,
                value: "1",
                name: "Broj prethodnih vlasnika"
              }, {
                id: 902,
                type: b,
                value: c,
                name: "Servisna knjiga"
              }, {
                id: 1834,
                type: b,
                value: c,
                name: "Tempomat"
              }, {
                id: 2416,
                type: b,
                value: c,
                name: "ABS"
              }, {
                id: 54,
                type: b,
                value: c,
                name: "Servo volan"
              }, {
                id: 1836,
                type: b,
                value: c,
                name: "Komande na volanu"
              }, {
                id: 2417,
                type: b,
                value: c,
                name: "ESP"
              }, {
                id: 53,
                type: b,
                value: c,
                name: "Airbag"
              }, {
                id: A,
                type: b,
                value: c,
                name: "El. podizači stakala"
              }, {
                id: 58,
                type: b,
                value: c,
                name: "Električni retrovizori"
              }, {
                id: 51,
                type: b,
                value: c,
                name: "Klima"
              }, {
                id: 2418,
                type: b,
                value: "Dvozonska",
                name: "Višezonska klima"
              }, {
                id: 2972,
                type: b,
                value: c,
                name: "Digitalna klima"
              }, {
                id: 5258,
                type: b,
                value: c,
                name: "Touch screen (ekran)"
              }, {
                id: 65,
                type: b,
                value: c,
                name: "Navigacija"
              }, {
                id: 4991,
                type: b,
                value: c,
                name: "Grijanje sjedišta"
              }, {
                id: 6681,
                type: b,
                value: c,
                name: "El. pomjeranje sjedišta"
              }, {
                id: 6682,
                type: b,
                value: c,
                name: "Senzor auto. svjetla"
              }, {
                id: 67,
                type: b,
                value: c,
                name: "Alu felge"
              }, {
                id: 55,
                type: b,
                value: c,
                name: "Alarm"
              }, {
                id: 4727,
                type: b,
                value: c,
                name: "Centralna brava"
              }, {
                id: 56,
                type: b,
                value: c,
                name: "Daljinsko otključavanje"
              }, {
                id: 4167,
                type: b,
                value: "5",
                name: "Sjedećih mjesta"
              }, {
                id: 4759,
                type: b,
                value: c,
                name: "Auto kuka"
              }, {
                id: 5227,
                type: b,
                value: c,
                name: "ISOFIX"
              }],
              model_id: B,
              category_id: m,
              categories_all: [{
                id: g,
                name: "Vozila"
              }, {
                id: m,
                name: n
              }],
              images_old: [{
                path: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5c03c843f",
                url: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5c03c843f-velika.jpg",
                highlighted: a
              }, {
                path: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5d21c1f7e",
                url: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5d21c1f7e-velika.jpg",
                highlighted: a
              }, {
                path: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5d2748fdc",
                url: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5d2748fdc-velika.jpg",
                highlighted: a
              }, {
                path: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5d2eea956",
                url: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5d2eea956-velika.jpg",
                highlighted: a
              }, {
                path: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5c6cd7de6",
                url: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5c6cd7de6-velika.jpg",
                highlighted: a
              }, {
                path: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5c71d5f21",
                url: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5c71d5f21-velika.jpg",
                highlighted: a
              }, {
                path: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5c757250e",
                url: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5c757250e-velika.jpg",
                highlighted: a
              }, {
                path: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5c7855929",
                url: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5c7855929-velika.jpg",
                highlighted: a
              }, {
                path: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5c7d2486f",
                url: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5c7d2486f-velika.jpg",
                highlighted: a
              }, {
                path: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5c80a60ff",
                url: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5c80a60ff-velika.jpg",
                highlighted: a
              }, {
                path: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5c83cae3c",
                url: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5c83cae3c-velika.jpg",
                highlighted: a
              }, {
                path: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5c8e881e0",
                url: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5c8e881e0-velika.jpg",
                highlighted: a
              }, {
                path: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5c93b4309",
                url: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5c93b4309-velika.jpg",
                highlighted: a
              }, {
                path: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5d3d254c6",
                url: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5d3d254c6-velika.jpg",
                highlighted: a
              }, {
                path: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5d49a106c",
                url: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5d49a106c-velika.jpg",
                highlighted: a
              }, {
                path: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5d4f31ea8",
                url: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5d4f31ea8-velika.jpg",
                highlighted: a
              }, {
                path: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5d5af162b",
                url: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5d5af162b-velika.jpg",
                highlighted: a
              }, {
                path: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5d629e7de",
                url: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5d629e7de-velika.jpg",
                highlighted: a
              }, {
                path: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5d696f594",
                url: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5d696f594-velika.jpg",
                highlighted: a
              }, {
                path: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5d70462c8",
                url: "https:\u002F\u002Fs9.pik.ba\u002Fgalerija\u002F2023-02\u002F15\u002F05\u002Fslika-1055467-63ec5d70462c8-velika.jpg",
                highlighted: a
              }],
              images: ["https:\u002F\u002Fd4n0y8dshd77z.cloudfront.net\u002Flistings\u002F51829903\u002Flg\u002FOLX-7e179d32377e.ba28897350024829jpg", "https:\u002F\u002Fd4n0y8dshd77z.cloudfront.net\u002Flistings\u002F51829903\u002Flg\u002FOLX-6d2dbedd6926.ba25426657343628jpg", "https:\u002F\u002Fd4n0y8dshd77z.cloudfront.net\u002Flistings\u002F51829903\u002Flg\u002FOLX-83e274bb9719.ba12057583432245jpg", "https:\u002F\u002Fd4n0y8dshd77z.cloudfront.net\u002Flistings\u002F51829903\u002Flg\u002FOLX-dee136c94871.ba67072543993572jpg", "https:\u002F\u002Fd4n0y8dshd77z.cloudfront.net\u002Flistings\u002F51829903\u002Flg\u002FOLX-04eac1fc9d41.ba43988758108018jpg", "https:\u002F\u002Fd4n0y8dshd77z.cloudfront.net\u002Flistings\u002F51829903\u002Flg\u002FOLX-23716a1aa839.ba64333528638402jpg", "https:\u002F\u002Fd4n0y8dshd77z.cloudfront.net\u002Flistings\u002F51829903\u002Flg\u002FOLX-52f89cf36709.ba31951814370404jpg", "https:\u002F\u002Fd4n0y8dshd77z.cloudfront.net\u002Flistings\u002F51829903\u002Flg\u002FOLX-b0955ac4d16f.ba77623657450733jpg", "https:\u002F\u002Fd4n0y8dshd77z.cloudfront.net\u002Flistings\u002F51829903\u002Flg\u002FOLX-a8c206d1893a.ba49109574499520jpg", "https:\u002F\u002Fd4n0y8dshd77z.cloudfront.net\u002Flistings\u002F51829903\u002Flg\u002FOLX-93e6658df53d.ba99355978528108jpg", "https:\u002F\u002Fd4n0y8dshd77z.cloudfront.net\u002Flistings\u002F51829903\u002Flg\u002FOLX-d1fa33900ce6.ba21475353204763jpg", "https:\u002F\u002Fd4n0y8dshd77z.cloudfront.net\u002Flistings\u002F51829903\u002Flg\u002FOLX-423ab11da0f7.ba73029474920885jpg", "https:\u002F\u002Fd4n0y8dshd77z.cloudfront.net\u002Flistings\u002F51829903\u002Flg\u002FOLX-18ffb6e443f9.ba40810139620790jpg", "https:\u002F\u002Fd4n0y8dshd77z.cloudfront.net\u002Flistings\u002F51829903\u002Flg\u002FOLX-b49ab8df7c5d.ba52212868872027jpg", "https:\u002F\u002Fd4n0y8dshd77z.cloudfront.net\u002Flistings\u002F51829903\u002Flg\u002FOLX-0b83613a9283.ba37651594950527jpg", "https:\u002F\u002Fd4n0y8dshd77z.cloudfront.net\u002Flistings\u002F51829903\u002Flg\u002FOLX-1d1080b7af0a.ba88663107868727jpg", "https:\u002F\u002Fd4n0y8dshd77z.cloudfront.net\u002Flistings\u002F51829903\u002Flg\u002FOLX-cd98eb1f9d0a.ba82386339265518jpg", "https:\u002F\u002Fd4n0y8dshd77z.cloudfront.net\u002Flistings\u002F51829903\u002Flg\u002FOLX-4e9b367a3764.ba69453318731185jpg", "https:\u002F\u002Fd4n0y8dshd77z.cloudfront.net\u002Flistings\u002F51829903\u002Flg\u002FOLX-4dedc358a359.ba53833979228000jpg", "https:\u002F\u002Fd4n0y8dshd77z.cloudfront.net\u002Flistings\u002F51829903\u002Flg\u002FOLX-40b55ec487a2.ba50212927453490jpg", "https:\u002F\u002Fd4n0y8dshd77z.cloudfront.net\u002Flistings\u002F51829903\u002Flg\u002FOLX-cb17d1a519a9.ba18585315245663jpg", "https:\u002F\u002Fd4n0y8dshd77z.cloudfront.net\u002Flistings\u002F51829903\u002Flg\u002FOLX-3f8d878e48d4.ba13034192907738jpg"],
              cities: [{
                id: s,
                name: t,
                location: {
                  lat: u,
                  lon: v
                },
                canton_id: j
              }],
              category: {
                id: m,
                name: n,
                name_singular: n,
                slug: "automobili",
                parent_id: g,
                order: g,
                top_category: a,
                highlighted: a,
                shipping_available: a,
                sensitive_content: a,
                post_option: e,
                show_price: f,
                show_brand: f,
                brand_required: a,
                model_required: a,
                has_models: a,
                show_condition: f,
                show_map: a,
                listing_fee: 50,
                base_listing_price: A,
                icon: e
              },
              brand: {
                id: 89,
                name: "Volkswagen",
                slug: "volkswagen"
              },
              model: {
                id: B,
                name: "Tiguan",
                slug: "tiguan"
              },
              date: 1676837720,
              sku_number: e,
              created_at: 1676434437
            },
            error: e,
            user: r
          }],
          fetch: {},
          error: e,
          state: {
            categories: {
              categories: [],
              customPageCategories: new Map([]),
              allCategories: [],
              activeCategory: e
            },
            mobileHeaderbar: {
              sticky: f,
              logoVisible: f,
              saveVisible: a
            },
            user: {
              user: e
            },
            search: {
              filters: {
                attr: {}
              },
              showMap: a,
              showBrands: a,
              results: [],
              attributes: [],
              meta: e,
              aggregations: e,
              lastCategory: h,
              loaded: f,
              autoSuggests: []
            },
            multiListing: {
              filters: {
                attr: {}
              },
              showMap: a,
              showBrands: a,
              results: [],
              attributes: [],
              meta: e,
              aggregations: e,
              lastCategory: h,
              loaded: f
            },
            messages: {
              conversations: [],
              meta: d
            },
            locations: {
              locations: [],
              cities: [],
              updatedResults: []
            },
            listing: {
              creation: {
                options: [{
                  id: m,
                  title: "Automobil",
                  buttonColor: "#3276BF",
                  icon: "car",
                  type: "selling",
                  url: "vozila\u002F18"
                }, {
                  id: g,
                  title: "Nekretnine",
                  buttonColor: "#6A9F42",
                  icon: "nekretnina",
                  type: "renting",
                  url: "nekretnine"
                }, {
                  id: i,
                  title: "Usluge",
                  buttonColor: "#B56C7B",
                  icon: "usluge",
                  type: "job",
                  url: o
                }, {
                  id: l,
                  title: "Poslovi",
                  buttonColor: "#F5D24A",
                  icon: "posao",
                  type: "services",
                  url: o
                }, {
                  id: j,
                  title: "Ostalo",
                  buttonColor: "#FC7B07",
                  icon: "\u002F_nuxt\u002Fimg\u002Fostalo.aa4b71b.png",
                  type: "gift",
                  url: o
                }],
                categoryAttributeRules: {
                  automobili: {
                    required: [{
                      id: i,
                      name: "godište",
                      order: h
                    }, {
                      id: l,
                      name: "kilometraža",
                      order: g
                    }, {
                      id: z,
                      name: "kubikaža",
                      order: i
                    }, {
                      id: y,
                      name: "gorivo",
                      order: l
                    }, {
                      id: x,
                      name: "broj-vrata",
                      order: j
                    }]
                  }
                },
                standardAttributes: [{
                  display_name: "Stanje",
                  name: "status",
                  type: C,
                  options: [{
                    text: "Novo",
                    value: "new"
                  }, {
                    text: "Koristeno",
                    value: w
                  }],
                  value: d
                }, {
                  display_name: "Vrsta oglasa",
                  name: "article_type",
                  type: C,
                  options: [{
                    text: "Samo prodaja",
                    value: "sales"
                  }, {
                    text: "Samo iznajmljivanje",
                    value: "rent"
                  }, {
                    text: "Samo potraznja",
                    value: "request"
                  }],
                  value: d
                }],
                siteVisibilityOptions: [{
                  label: p,
                  img: "standardna-vidljivost.svg",
                  customRadioStyle: d,
                  customLabelStyle: d,
                  additionalLabel: p
                }, {
                  label: "Izdvojen oglas na vrhu kategorije, istaknut premium bojom.",
                  img: "izdvojen-u-kategorija.svg",
                  customRadioStyle: d,
                  customLabelStyle: d
                }, {
                  label: "Izdvojen oglas na naslovnoj i vrhu kategorije, istaknut premium+ bojom.",
                  img: "izdvojen-vrh.svg",
                  customRadioStyle: d,
                  customLabelStyle: d
                }],
                visibilityRenewalOptions: [{
                  label: "Bez automatskog obnavljanja (GRATIS)",
                  img: d,
                  customRadioStyle: d,
                  customLabelStyle: d,
                  additionalLabel: p
                }, {
                  label: "Automatsko obnavljanje svaki dan na vrh izdvojenih u kategoriji i naslovnici (+50% od cijene izdvajanja)",
                  img: d,
                  customRadioStyle: d,
                  customLabelStyle: d
                }, {
                  label: "Automatsko obnavljanje svaka 3 sata na vrh izdvojenih u kategoriji i naslovnici (+200% od cijene izdvajanja)",
                  img: d,
                  customRadioStyle: d,
                  customLabelStyle: d
                }],
                additionalFeatures: [{
                  display_name: "Hitna prodaja oglasa",
                  name: "urgent",
                  type: D
                }, {
                  display_name: "Istakni naslov oglasa u pretrazi",
                  name: "highlighted",
                  type: D
                }],
                titleAttribute: {
                  display_name: "Naslov oglasa",
                  name: "title",
                  type: E
                },
                priceAttribute: {
                  display_name: "Cijena",
                  name: "price",
                  type: E
                },
                category: {},
                categoryAttributes: [],
                categoryRequiredAttributes: [],
                categoryAdditionalCheckboxAttributes: [],
                categoryAdditionalInputAttributes: [],
                listing: {
                  quantity: g,
                  location: {
                    lat: "43.1235",
                    lon: "42.5426"
                  },
                  city_id: g,
                  active: f,
                  attributes: []
                }
              },
              defaultCreation: {
                title: d
              },
              feedback: {
                feedbacks: []
              },
              highlighted: {
                highlightedListings: [],
                loading: a,
                loaded: a,
                page: g,
                totalListings: h,
                meta: {},
                currentCategory: d
              },
              highlightedNew: {
                highlightedListingsNew: []
              },
              preview: {
                listing: e,
                listingAttributes: [],
                savedArticleMessage: d,
                removeFromFavoritesMessage: d,
                updateSaved: d,
                showMap: a,
                failed: a
              },
              questions: {
                questions: [],
                totalQuestions: h,
                meta: e
              }
            },
            auth: {
              user: e,
              loggedIn: a,
              strategy: "laravelSanctum"
            }
          },
          serverRendered: f,
          routePath: "\u002Fartikal\u002F51829903\u002Fvw-tiguan-4motion-20-tdi-2012-god",
          config: {
            _app: {
              basePath: "\u002F",
              assetsPath: "\u002F_nuxt\u002F",
              cdnURL: e
            }
          },
          routesDirectory: "root-domain"
        }
      }(false, "string", "true", "", null, true, 1, 0, 2, 4, "number", 3, 18, "Automobili", "opisi-oglas", "Standardna objava oglasa, standardna boja oglasa.", "VW TIGUAN 4MOTION 2.0 TDI 2012 god.", {}, 39, "Visoko", "43.9890587", "18.1817776", "used", 901, 7, 1144, 15, 1620, "select", "checkbox", "text"));
    </script>
"""


match = re.search(r"data:\s*\[[^[\]]*(?:\[[^[\]]*\][^[\]]*)*\](?=,?\s*fetch)", text, re.DOTALL)
results = match.group(0)


match2 = re.search(r"attributes:(.*?)(?=model_id:)", results, re.DOTALL)
attr = match2.group(0)
print(attr)