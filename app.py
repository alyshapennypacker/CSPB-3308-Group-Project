from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    # Render HTML with count variable
    return render_template("index.html")

@app.route("/aboutus")
def about_us():
    return render_template("about_us.html")

@app.route("/addstreaming")
def add_streaming():
    return render_template("add_streaming.html")

@app.route("/allinstructor")
def all_instructor():
    return render_template("all_instructor.html")

@app.route("/applyjob")
def apply_job():
    return render_template("apply_job.html")

@app.route("/blogsingleview")
def blog_single_view():
    return render_template("blog_single_view.html")

@app.route("/career")
def career():
    return render_template("career.html")

@app.route("/certificationcenter")
def certification_center():
    return render_template("certification_center.html")

@app.route("/certificationstartform")
def certification_start_form():
    return render_template("certification_start_form.html")

@app.route("/certificationtestresult")
def certification_test_result():
    return render_template("certification_test_result.html")

@app.route("/certificationtestview")
def certification_test_view():
    return render_template("certification_test_view.html")

@app.route("/checkoutcourse")
def checkout_course():
    return render_template("checkout_course.html")

@app.route("/checkoutmembership")
def checkout_membership():
    return render_template("checkout_membership.html")

@app.route("/comingsoon")
def coming_soon():
    return render_template("coming_soon.html")

@app.route("/companydetails")
def company_details():
    return render_template("company_details.html")

@app.route("/contactus")
def contact_us():
    return render_template("contact_us.html")

@app.route("/coursedetailview")
def course_detail_view():
    return render_template("course_detail_view.html")

@app.route("/createnewcourse")
def create_new_course():
    return render_template("create_new_course.html")

@app.route("/error404")
def error_404():
    return render_template("error_404.html")

@app.route("/explore")
def explore():
    return render_template("explore.html")

@app.route("/feedback")
def feedback():
    return render_template("feedback.html")

@app.route("/forgotpassword")
def forgot_password():
    return render_template("forgot_password.html")

@app.route("/help")
def help():
    return render_template("help.html")

@app.route("/helpfaqview")
def help_faq_view():
    return render_template("help_faq_view.html")

@app.route("/helpinstructorfaq")
def help_instructor_faq():
    return render_template("help_instructor_faq.html")

@app.route("/instructorallreviews")
def instructor_all_reviews():
    return render_template("instructor_all_reviews.html")

@app.route("/instructoranalyics")
def instructor_analyics():
    return render_template("instructor_analyics.html")

@app.route("/instructorcourses")
def instructor_courses():
    return render_template("instructor_courses.html")

@app.route("/instructordashboard")
def instructor_dashboard():
    return render_template("instructor_dashboard.html")

@app.route("/instructorearning")
def instructor_earning():
    return render_template("instructor_earning.html")

@app.route("/instructormessages")
def instructor_messages():
    return render_template("instructor_messages.html")

@app.route("/instructormycertificates")
def instructor_my_certificates():
    return render_template("instructor_my_certificates.html")

@app.route("/instructornotifications")
def instructor_notifications():
    return render_template("instructor_notifications.html")

@app.route("/instructorpayout")
def instructor_payout():
    return render_template("instructor_payout.html")

@app.route("/instructorprofileview")
def instructor_profile_view():
    return render_template("instructor_profile_view.html")

@app.route("/instructorstatements")
def instructor_statements():
    return render_template("instructor_statements.html")

@app.route("/instructorverification")
def instructor_verification():
    return render_template("instructor_verification.html")

@app.route("/invoice")
def invoice():
    return render_template("invoice.html")

@app.route("/liveoutput")
def live_output():
    return render_template("live_output.html")

@app.route("/livestreams")
def live_streams():
    return render_template("live_streams.html")

@app.route("/membership")
def membership():
    return render_template("membership.html")

@app.route("/myinstructorprofileview")
def my_instructor_profile_view():
    return render_template("my_instructor_profile_view.html")

@app.route("/mystudentprofileview")
def my_student_profile_view():
    return render_template("my_student_profile_view.html")

@app.route("/ourblog")
def our_blog():
    return render_template("our_blog.html")

@app.route("/press")
def press():
    return render_template("press.html")

@app.route("/reporthistory")
def report_history():
    return render_template("report_history.html")

@app.route("/savedcourses")
def saved_courses():
    return render_template("saved_courses.html")

@app.route("/searchresult")
def search_result():
    return render_template("search_result.html")

@app.route("/setting")
def setting():
    return render_template("setting.html")

@app.route("/shoppingcart")
def shopping_cart():
    return render_template("shopping_cart.html")

@app.route("/signin")
def sign_in():
    return render_template("sign_in.html")

@app.route("/signup")
def sign_up():
    return render_template("sign_up.html")

@app.route("/signupsteps")
def sign_up_steps():
    return render_template("sign_up_steps.html")

@app.route("/sitemap")
def sitemap():
    return render_template("sitemap.html")

@app.route("/studentallreviews")
def student_all_reviews():
    return render_template("student_all_reviews.html")

@app.route("/studentcourses")
def student_courses():
    return render_template("student_courses.html")

@app.route("/studentcredits")
def student_credits():
    return render_template("student_credits.html")

@app.route("/studentdashboard")
def student_dashboard():
    return render_template("student_dashboard.html")

@app.route("/studentmessages")
def student_messages():
    return render_template("student_messages.html")

@app.route("/studentmycertificates")
def student_my_certificates():
    return render_template("student_my_certificates.html")

@app.route("/studentnotifications")
def student_notifications():
    return render_template("student_notifications.html")

@app.route("/studentstatements")
def student_statements():
    return render_template("student_statements.html")

@app.route("/termsofuse")
def terms_of_use():
    return render_template("terms_of_use.html")

@app.route("/thankyou")
def thank_you():
    return render_template("thank_you.html")












@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/landing")
def landing():
    return render_template("landing.html")

@app.route("/register")
def register():
    return render_template("register.html")

if __name__ == "__main__":
    app.run()