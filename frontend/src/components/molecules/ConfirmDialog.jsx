/**
 * ConfirmDialog Molecule - Diálogo de confirmación
 */
import Modal from '../atoms/Modal'
import Button from '../atoms/Button'

const ConfirmDialog = ({
  isOpen,
  onClose,
  onConfirm,
  title = '¿Estás seguro?',
  message = 'Esta acción no se puede deshacer.',
  confirmText = 'Confirmar',
  cancelText = 'Cancelar',
  variant = 'danger',
  isLoading = false,
}) => {
  const variantStyles = {
    danger: {
      icon: (
        <svg
          className="w-12 h-12 text-red-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
          />
        </svg>
      ),
      buttonVariant: 'primary',
      buttonClass: 'bg-red-500 hover:bg-red-600 text-white',
    },
    warning: {
      icon: (
        <svg
          className="w-12 h-12 text-amber-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
      ),
      buttonVariant: 'primary',
      buttonClass: 'bg-amber-500 hover:bg-amber-600 text-slate-950',
    },
    info: {
      icon: (
        <svg
          className="w-12 h-12 text-blue-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
      ),
      buttonVariant: 'primary',
      buttonClass: '',
    },
  }

  const style = variantStyles[variant] || variantStyles.info

  return (
    <Modal isOpen={isOpen} onClose={onClose} size="sm" showCloseButton={false}>
      <div className="text-center">
        <div className="flex justify-center mb-4">
          {style.icon}
        </div>
        <h3 className="text-lg font-display font-bold text-white mb-2">
          {title}
        </h3>
        <p className="text-white/60 mb-6">
          {message}
        </p>
        <div className="flex gap-3 justify-center">
          <Button
            variant="ghost"
            onClick={onClose}
            disabled={isLoading}
          >
            {cancelText}
          </Button>
          <Button
            onClick={onConfirm}
            disabled={isLoading}
            className={style.buttonClass}
          >
            {isLoading ? 'Procesando...' : confirmText}
          </Button>
        </div>
      </div>
    </Modal>
  )
}

export default ConfirmDialog
