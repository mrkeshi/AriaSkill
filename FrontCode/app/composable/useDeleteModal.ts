/**
 * useDeleteModal<T>
 *
 * Generic composable for the confirm-before-delete pattern.
 * Replaces the repetitive trio:
 *   const deleteModal  = ref(false)
 *   const selectedItem = ref<T | null>(null)
 *   const openDelete   = (item: T) => { selectedItem.value = item; deleteModal.value = true }
 *
 * Usage (object):
 *   const { deleteModal, selectedItem, openDelete, closeDelete } = useDeleteModal<ProjectDTO>()
 *
 * Usage (primitive id):
 *   const { deleteModal, selectedItem: selectedId, openDelete } = useDeleteModal<number>()
 */
export const useDeleteModal = <T>() => {
  const deleteModal  = ref(false)
  const selectedItem = ref<T | null>(null) as Ref<T | null>

  const openDelete = (item: T) => {
    selectedItem.value = item
    deleteModal.value  = true
  }

  const closeDelete = () => {
    deleteModal.value  = false
    selectedItem.value = null
  }

  return { deleteModal, selectedItem, openDelete, closeDelete }
}
