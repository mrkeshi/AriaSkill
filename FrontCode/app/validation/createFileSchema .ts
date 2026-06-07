import * as yup from 'yup'

interface FileOptions {
  required?: boolean
  maxSizeMB?: number
  allowedTypes?: string[]
}

export const createFileSchema = ({
  required = true,
  maxSizeMB = 2,
  allowedTypes = []
}: FileOptions) => {
  const MAX_SIZE = maxSizeMB * 1024 * 1024

  let schema = yup.mixed<File>()

  if (required) {
    schema = schema.required('انتخاب فایل الزامی است')
  }

  return schema
    .test('fileType', 'فرمت فایل مجاز نیست', (value) => {
      if (!value) return !required
      if (!allowedTypes.length) return true
      return allowedTypes.includes(value.type)
    })
    .test('fileSize', `حداکثر حجم فایل ${maxSizeMB} مگابایت است`, (value) => {
      if (!value) return !required
      return value.size <= MAX_SIZE
    })
}
