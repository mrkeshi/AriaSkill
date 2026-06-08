import { createFileSchema } from "../createFileSchema ";
import * as Yup from 'yup'
/** Validation schema for the user profile editing form, featuring custom avatar file constraints. */
export const editUserSchema = Yup.object({
  avatar: createFileSchema({
    required: false,
    maxSizeMB: 2,
    allowedTypes: ['image/jpeg', 'image/png']
  }),
  username: Yup.string().required('Username is required'),
  first_name: Yup.string().required('First name is required'),
  last_name: Yup.string().required('Last name is required'),
  job_title: Yup.string().required('Job title is required'),
  about_me: Yup.string().required('About me is required'),
  linkedin_link: Yup.string().nullable(),
  instagram_link: Yup.string().nullable(),
  discord_link: Yup.string().nullable(),
  telegram_link: Yup.string().nullable(),
})
