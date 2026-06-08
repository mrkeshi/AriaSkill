import * as Yup from 'yup'
// Comment Schema for Validation
export const ResetPassowrdWithEmailSchema = Yup.object().shape({
  email: Yup.string()
    .email('ایمیل باید معتبر باشد')
    .required('لطفا ایمیل خود را وارد کنید.'),
})

export const SendCommentSchema = Yup.object().shape({
  message: Yup.string()
    .required('لطفا متن نظر را وارد کنید.')
    .min(10, 'طول کامنت حداقل باید ده کاراکتر باشد')
    .max(300, 'طول کامنت باید حداکثر سیصد کاراکتر باشد'),
})
