from app.core.database import SessionLocal
from app.models.models import CareerPath
from sqlalchemy.orm import Session

CAREERS = [
    {
        "model_index": 0,
        "title": "Accountant",
        "description": "Mengelola laporan keuangan, audit, dan perpajakan perusahaan.",
        "required_skills": "Accounting, Financial Analysis, Excel",
        "industry": "Finance",
        "avg_salary_idr": "5jt - 15jt",
    },
    {
        "model_index": 1,
        "title": "Artist",
        "description": "Membuat karya seni visual, ilustrasi, atau media kreatif.",
        "required_skills": "Creativity, Design, Communication",
        "industry": "Creative",
        "avg_salary_idr": "4jt - 20jt",
    },
    {
        "model_index": 2,
        "title": "Banker",
        "description": "Mengelola layanan keuangan dan investasi di sektor perbankan.",
        "required_skills": "Finance, Communication, Analysis",
        "industry": "Banking",
        "avg_salary_idr": "6jt - 20jt",
    },
    {
        "model_index": 3,
        "title": "Business Owner",
        "description": "Membangun dan mengelola bisnis sendiri.",
        "required_skills": "Leadership, Marketing, Communication",
        "industry": "Business",
        "avg_salary_idr": "Tidak terbatas",
    },
    {
        "model_index": 4,
        "title": "Construction Engineer",
        "description": "Merancang dan mengawasi proyek konstruksi.",
        "required_skills": "Physics, Engineering, Problem Solving",
        "industry": "Construction",
        "avg_salary_idr": "6jt - 18jt",
    },
    {
        "model_index": 5,
        "title": "Designer",
        "description": "Mendesain visual produk, UI/UX, atau media digital.",
        "required_skills": "Creativity, Design Tools, Communication",
        "industry": "Creative",
        "avg_salary_idr": "5jt - 15jt",
    },
    {
        "model_index": 6,
        "title": "Doctor",
        "description": "Memberikan layanan kesehatan kepada pasien.",
        "required_skills": "Biology, Counseling, Communication",
        "industry": "Healthcare",
        "avg_salary_idr": "8jt - 30jt",
    },
    {
        "model_index": 7,
        "title": "Game Developer",
        "description": "Mengembangkan game berbasis desktop, mobile, atau web.",
        "required_skills": "Programming, Logic, Creativity",
        "industry": "Technology",
        "avg_salary_idr": "6jt - 25jt",
    },
    {
        "model_index": 8,
        "title": "Government Officer",
        "description": "Bekerja dalam instansi pemerintahan dan pelayanan publik.",
        "required_skills": "Administration, Communication",
        "industry": "Government",
        "avg_salary_idr": "5jt - 15jt",
    },
    {
        "model_index": 9,
        "title": "Lawyer",
        "description": "Memberikan bantuan hukum dan advokasi.",
        "required_skills": "Communication, Critical Thinking",
        "industry": "Law",
        "avg_salary_idr": "7jt - 25jt",
    },
    {
        "model_index": 10,
        "title": "Real Estate Developer",
        "description": "Mengembangkan bisnis properti dan real estate.",
        "required_skills": "Marketing, Finance, Communication",
        "industry": "Property",
        "avg_salary_idr": "7jt - 30jt",
    },
    {
        "model_index": 11,
        "title": "Scientist",
        "description": "Melakukan penelitian dan eksperimen ilmiah.",
        "required_skills": "Research, Data Analysis, Critical Thinking",
        "industry": "Research",
        "avg_salary_idr": "6jt - 20jt",
    },
    {
        "model_index": 12,
        "title": "Social Network Studies",
        "description": "Menganalisis perilaku sosial dan hubungan masyarakat.",
        "required_skills": "Communication, Analysis",
        "industry": "Social",
        "avg_salary_idr": "5jt - 12jt",
    },
    {
        "model_index": 13,
        "title": "Software Engineer",
        "description": "Mengembangkan sistem dan aplikasi perangkat lunak.",
        "required_skills": "Python, SQL, Machine Learning",
        "industry": "Technology",
        "avg_salary_idr": "7jt - 30jt",
    },
    {
        "model_index": 14,
        "title": "Stock Investor",
        "description": "Menganalisis dan melakukan investasi pasar saham.",
        "required_skills": "Financial Analysis, Data Analysis",
        "industry": "Finance",
        "avg_salary_idr": "Variatif",
    },
    {
        "model_index": 15,
        "title": "Teacher",
        "description": "Mengajar dan membimbing siswa dalam pendidikan.",
        "required_skills": "Communication, Counseling",
        "industry": "Education",
        "avg_salary_idr": "4jt - 12jt",
    },
    {
        "model_index": 16,
        "title": "Writer",
        "description": "Menulis artikel, buku, atau konten digital.",
        "required_skills": "Writing, Creativity, Communication",
        "industry": "Media",
        "avg_salary_idr": "4jt - 15jt",
    },
]


def seed_careers() -> None:
    db: Session = SessionLocal()

    try:
        existing = db.query(CareerPath).count()

        if existing > 0:
            print("career_paths sudah terisi")
            return

        for career in CAREERS:
            db.add(CareerPath(**career))

        db.commit()

        print("Seed career_paths berhasil")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_careers()
