
import * as Yup from 'yup'


export const LoginSchema = Yup.object().shape({
  identifier: Yup.string().required("وارد کردن  نام کاربری یا ایمیل ضروری هست."),
  password: Yup.string()
    .required("وارد کردن پسورد الزامی هست")

})

export const ResetPassowrdWithEmailSchema = Yup.object().shape({
  email: Yup.string().email("ایمیل باید معتبر باشد").required("احمق لطفا ایمیل خودت رو درست وارد کن."),


})

export const ChangePasswordSchema = Yup.object().shape({
  password: Yup.string()
    .required("لطفا رمز عبور را وارد کنید")
    .min(6, "رمز عبور باید حداقل 6 کاراکتر باشد"),

  password_confirm: Yup.string()
    .required("لطفا تکرار رمز عبور را وارد کنید")
    .oneOf([Yup.ref("password")], "رمز عبور و تکرار آن یکسان نیستند"),
})


export const RegisterSchema = Yup.object().shape({
  username: Yup.string().required("وارد کردن  نام کاربری ضروری هست."),
  firstName: Yup.string().required("وارد کردن  نام  ضروری هست."),
  lastName:Yup.string().required("وارد کردن  نام خانوادگی ضروری هست."),
  email: Yup.string().email("ایمیل باید معتبر باشد").required("احمق لطفا ایمیل خودت رو درست وارد کن."),
  password: Yup.string()
    .required("لطفا رمز عبور را وارد کنید")
    .min(6, "رمز عبور باید حداقل 6 کاراکتر باشد"),
  password_confirm: Yup.string()
    .required("لطفا تکرار رمز عبور را وارد کنید")
    .oneOf([Yup.ref("password")], "رمز عبور و تکرار آن یکسان نیستند"),



})