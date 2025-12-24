/**
 * ParticleField Atom - Campo de partículas animadas
 * Efecto visual decorativo con partículas flotantes
 */
import { useEffect, useRef, useMemo } from 'react'

const ParticleField = ({
  particleCount = 50,
  colors = ['#32d5ff', '#a855f7', '#fcd34d'],
  minSize = 2,
  maxSize = 4,
  minSpeed = 0.2,
  maxSpeed = 0.8,
  className = '',
}) => {
  const canvasRef = useRef(null)
  const animationRef = useRef(null)
  const particlesRef = useRef([])

  // Generar partículas iniciales
  const initParticles = useMemo(() => {
    return (width, height) => {
      const particles = []
      for (let i = 0; i < particleCount; i++) {
        particles.push({
          x: Math.random() * width,
          y: Math.random() * height,
          size: minSize + Math.random() * (maxSize - minSize),
          speedX: (Math.random() - 0.5) * maxSpeed,
          speedY: (Math.random() - 0.5) * maxSpeed,
          color: colors[Math.floor(Math.random() * colors.length)],
          opacity: 0.1 + Math.random() * 0.4,
        })
      }
      return particles
    }
  }, [particleCount, colors, minSize, maxSize, maxSpeed])

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    let width = canvas.offsetWidth
    let height = canvas.offsetHeight

    // Set canvas size
    const setCanvasSize = () => {
      width = canvas.offsetWidth
      height = canvas.offsetHeight
      canvas.width = width * window.devicePixelRatio
      canvas.height = height * window.devicePixelRatio
      ctx.scale(window.devicePixelRatio, window.devicePixelRatio)
    }

    setCanvasSize()
    particlesRef.current = initParticles(width, height)

    // Animation loop
    const animate = () => {
      ctx.clearRect(0, 0, width, height)

      particlesRef.current.forEach((particle) => {
        // Update position
        particle.x += particle.speedX
        particle.y += particle.speedY

        // Wrap around edges
        if (particle.x < 0) particle.x = width
        if (particle.x > width) particle.x = 0
        if (particle.y < 0) particle.y = height
        if (particle.y > height) particle.y = 0

        // Draw particle
        ctx.beginPath()
        ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2)
        ctx.fillStyle = particle.color
        ctx.globalAlpha = particle.opacity
        ctx.fill()

        // Draw glow
        ctx.beginPath()
        ctx.arc(particle.x, particle.y, particle.size * 3, 0, Math.PI * 2)
        const gradient = ctx.createRadialGradient(
          particle.x,
          particle.y,
          0,
          particle.x,
          particle.y,
          particle.size * 3
        )
        gradient.addColorStop(0, particle.color)
        gradient.addColorStop(1, 'transparent')
        ctx.fillStyle = gradient
        ctx.globalAlpha = particle.opacity * 0.3
        ctx.fill()
      })

      ctx.globalAlpha = 1
      animationRef.current = requestAnimationFrame(animate)
    }

    animate()

    // Handle resize
    const handleResize = () => {
      setCanvasSize()
      particlesRef.current = initParticles(width, height)
    }

    window.addEventListener('resize', handleResize)

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
      }
      window.removeEventListener('resize', handleResize)
    }
  }, [initParticles])

  return (
    <canvas
      ref={canvasRef}
      className={`absolute inset-0 pointer-events-none ${className}`}
      style={{ width: '100%', height: '100%' }}
    />
  )
}

export default ParticleField
