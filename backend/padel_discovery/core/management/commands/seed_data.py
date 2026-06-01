from __future__ import annotations

from datetime import date, timedelta

from django.core.management.base import BaseCommand

from padel_discovery.core.models import Coach, Court, Tournament


COURTS = [
    ("Ace Arena Whitefield", "Whitefield Main Road", "Bangalore", "Karnataka", 12.9698, 77.7500, 750, "+91 90001 10001", "https://acearena.example.com", 4.8, "Premium indoor padel courts with coaching and cafe."),
    ("Smash Point Koramangala", "5th Block, Koramangala", "Bangalore", "Karnataka", 12.9352, 77.6245, 850, "+91 90001 10002", "https://smashpoint.example.com", 4.7, "Popular social court for after-work matches."),
    ("Urban Padel HSR", "Sector 2, HSR Layout", "Bangalore", "Karnataka", 12.9116, 77.6389, 700, "+91 90001 10003", "https://urbanpadel.example.com", 4.6, "Fast courts and beginner-friendly sessions."),
    ("Net Rush Andheri", "Andheri West", "Mumbai", "Maharashtra", 19.1364, 72.8277, 950, "+91 90001 10004", "https://netrush.example.com", 4.7, "Indoor courts close to the metro."),
    ("Coastline Padel Bandra", "Bandra West", "Mumbai", "Maharashtra", 19.0544, 72.8406, 1100, "+91 90001 10005", "https://coastline.example.com", 4.9, "Boutique venue with ocean breeze and pro shop."),
    ("Rally House Powai", "Powai Lake Road", "Mumbai", "Maharashtra", 19.1197, 72.9050, 800, "+91 90001 10006", "https://rallyhouse.example.com", 4.5, "Value-friendly court for everyday training."),
    ("Capital Padel Dwarka", "Sector 12, Dwarka", "Delhi", "Delhi", 28.5921, 77.0460, 650, "+91 90001 10007", "https://capitalpadel.example.com", 4.4, "Community-driven courts with evening slots."),
    ("Serve Zone Saket", "Saket District Centre", "Delhi", "Delhi", 28.5244, 77.2066, 900, "+91 90001 10008", "https://servezone.example.com", 4.6, "Covered courts with recovery lounge."),
    ("Northside Padel Gurugram", "Golf Course Extension", "Delhi", "Haryana", 28.4595, 77.0266, 1000, "+91 90001 10009", "https://northside.example.com", 4.8, "High-spec venue for leagues and coaching."),
    ("Deccan Smash", "Banjara Hills", "Hyderabad", "Telangana", 17.4065, 78.4772, 780, "+91 90001 10010", "https://deccansmash.example.com", 4.5, "Compact premium courts near central Hyderabad."),
    ("Hitech Padel", "Madhapur", "Hyderabad", "Telangana", 17.4505, 78.3915, 720, "+91 90001 10011", "https://hitechpadel.example.com", 4.7, "Corporate-friendly booking slots and lights."),
    ("Skyline Padel", "Gachibowli", "Hyderabad", "Telangana", 17.4401, 78.3489, 880, "+91 90001 10012", "https://skylinepadel.example.com", 4.6, "Modern venue near IT corridors."),
    ("Pune Padel Club", "Baner Road", "Pune", "Maharashtra", 18.5600, 73.7940, 700, "+91 90001 10013", "https://punepadel.example.com", 4.6, "Balanced pricing with training programs."),
    ("Apex Courts Kharadi", "Kharadi", "Pune", "Maharashtra", 18.5515, 73.9517, 760, "+91 90001 10014", "https://apexcourts.example.com", 4.7, "Busy venue for weekend ladders."),
    ("Riverfront Padel", "Wakad", "Pune", "Maharashtra", 18.5971, 73.7625, 680, "+91 90001 10015", "https://riverfront.example.com", 4.4, "Friendly venue with relaxed coaching sessions."),
    ("Baseline Padel Koramangala", "Koramangala 7th Block", "Bangalore", "Karnataka", 12.9335, 77.6241, 820, "+91 90001 10016", "https://baseline.example.com", 4.7, "Lifestyle club with courts and lounge."),
    ("Point 24 Juhu", "Juhu Tara Road", "Mumbai", "Maharashtra", 19.1025, 72.8260, 1200, "+91 90001 10017", "https://point24.example.com", 4.8, "Premium venue with private coaching bays."),
    ("Metro Rally Noida", "Sector 62", "Delhi", "Uttar Pradesh", 28.6139, 77.3910, 700, "+91 90001 10018", "https://metrorally.example.com", 4.5, "Easy access for NCR players."),
    ("CourtCraft Jubilee Hills", "Jubilee Hills", "Hyderabad", "Telangana", 17.4268, 78.4088, 840, "+91 90001 10019", "https://courtcraft.example.com", 4.7, "Stylish courts with digital booking."),
    ("ProSpin Padel", "Viman Nagar", "Pune", "Maharashtra", 18.5679, 73.9143, 730, "+91 90001 10020", "https://prospin.example.com", 4.6, "Good mix of social play and competition."),
]

COACHES = [
    ("Arjun Mehta", "Bangalore", 9, "beginner, advanced, footwork", "+91 91000 20001", "National-level coach focused on modern padel basics.", True),
    ("Priya Nair", "Bangalore", 7, "kids, beginner, doubles", "+91 91000 20002", "Known for patient junior programs and group clinics.", True),
    ("Rohan Kapoor", "Mumbai", 11, "advanced, smash, strategy", "+91 91000 20003", "Works with competitive players and league teams.", True),
    ("Sara Khan", "Mumbai", 6, "beginner, fitness, movement", "+91 91000 20004", "Great for adults returning to sport.", False),
    ("Manish Verma", "Delhi", 8, "beginner, tactics, consistency", "+91 91000 20005", "Drills-driven coach with a strong fundamentals focus.", True),
    ("Nida Shaikh", "Hyderabad", 10, "advanced, doubles, positioning", "+91 91000 20006", "Strong tactical coach for match play.", True),
    ("Aakash Iyer", "Pune", 5, "kids, beginner, cardio", "+91 91000 20007", "Youth coaching specialist with energetic sessions.", False),
    ("Neha Bhatia", "Pune", 12, "strategy, advanced, defense", "+91 91000 20008", "Helps players sharpen decision-making and court craft.", True),
    ("Kabir Joshi", "Hyderabad", 4, "beginner, social play, fitness", "+91 91000 20009", "Popular local coach for weekend batches.", False),
    ("Tanya Kulkarni", "Delhi", 13, "advanced, doubles, tournament prep", "+91 91000 20010", "Coaches players preparing for local tournaments.", True),
]

TOURNAMENTS = [
    ("Bangalore Open Ladder", "Bangalore", "Ace Arena Whitefield", 21, 5000, "Weekend ladder for all levels.", "https://events.example.com/bangalore-open"),
    ("Mumbai City Challenge", "Mumbai", "Coastline Padel Bandra", 28, 6500, "Fast-paced doubles tournament for club players.", "https://events.example.com/mumbai-city-challenge"),
    ("Delhi Smash Cup", "Delhi", "Serve Zone Saket", 35, 4500, "Friendly knockout format with prizes.", "https://events.example.com/delhi-smash-cup"),
    ("Hyderabad Weekend Warriors", "Hyderabad", "Hitech Padel", 14, 4000, "Open entry weekend tournament.", "https://events.example.com/hyderabad-weekend-warriors"),
    ("Pune Padel Premier", "Pune", "Pune Padel Club", 42, 6000, "Competitive event for club regulars.", "https://events.example.com/pune-padel-premier"),
    ("Whitefield Rising Stars", "Bangalore", "Baseline Padel Koramangala", 30, 3000, "Development tournament for improving players.", "https://events.example.com/whitefield-rising-stars"),
    ("Monsoon Masters", "Mumbai", "Point 24 Juhu", 49, 7000, "High-intensity event with sponsored prizes.", "https://events.example.com/monsoon-masters"),
    ("NCR Night Rally", "Delhi", "Metro Rally Noida", 56, 3500, "Evening matches designed for office players.", "https://events.example.com/ncr-night-rally"),
    ("Deccan Derby", "Hyderabad", "CourtCraft Jubilee Hills", 63, 5200, "City championship style event.", "https://events.example.com/deccan-derby"),
    ("Riverfront Rally", "Pune", "Riverfront Padel", 70, 2800, "Casual tournament with beginner and intermediate draws.", "https://events.example.com/riverfront-rally"),
]


class Command(BaseCommand):
    help = "Seed courts, coaches, and tournaments."

    def handle(self, *args, **options):
        courts_created = 0
        coaches_created = 0
        tournaments_created = 0

        for item in COURTS:
            _, created = Court.objects.update_or_create(
                name=item[0],
                defaults={
                    "address": item[1],
                    "city": item[2],
                    "state": item[3],
                    "latitude": item[4],
                    "longitude": item[5],
                    "hourly_price": item[6],
                    "phone": item[7],
                    "website": item[8],
                    "google_rating": item[9],
                    "description": item[10],
                },
            )
            courts_created += int(created)

        for item in COACHES:
            _, created = Coach.objects.update_or_create(
                name=item[0],
                defaults={
                    "city": item[1],
                    "experience_years": item[2],
                    "specialties": item[3],
                    "phone": item[4],
                    "bio": item[5],
                    "verified": item[6],
                },
            )
            coaches_created += int(created)

        base_date = date.today()
        for item in TOURNAMENTS:
            _, created = Tournament.objects.update_or_create(
                title=item[0],
                defaults={
                    "city": item[1],
                    "venue": item[2],
                    "date": base_date + timedelta(days=item[3]),
                    "entry_fee": item[4],
                    "description": item[5],
                    "registration_url": item[6],
                },
            )
            tournaments_created += int(created)

        self.stdout.write(self.style.SUCCESS(f"Seeded data: {courts_created} courts, {coaches_created} coaches, {tournaments_created} tournaments."))
