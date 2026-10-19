import { motion } from 'motion/react';
import { useState } from 'react';

type CharacterState = 'idle' | 'jump' | 'parry' | 'walk';

function CharacterDisplay({ state }: { state: CharacterState }) {
  const isJumping = state === 'jump';
  const isParrying = state === 'parry';
  const isIdle = state === 'idle';
  const isWalking = state === 'walk';

  return (
    <motion.svg
      width="128"
      height="128"
      viewBox="0 0 64 64"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      style={{ imageRendering: 'pixelated' }}
      animate={isJumping ? { y: [-24, 0, -24] } : {}}
      transition={
        isJumping
          ? {
              duration: 0.6,
              repeat: Infinity,
              ease: 'easeInOut',
            }
          : {}
      }
    >
      {/* Shadow */}
      <motion.ellipse
        cx="32"
        cy="58"
        rx="12"
        ry="4"
        fill="#000000"
        opacity={isJumping ? 0.2 : 0.4}
        animate={isJumping ? { scale: [0.6, 1.3, 0.6] } : {}}
        transition={isJumping ? { duration: 0.6, repeat: Infinity, ease: 'easeInOut' } : {}}
      />

      {/* Legs - Left leg */}
      <motion.g
        animate={
          isWalking
            ? { y: [0, -4, 0, 2, 0], rotate: [0, -8, 0, 4, 0] }
            : isIdle
            ? { rotate: [0, 1, 0] }
            : {}
        }
        transition={
          isWalking
            ? { duration: 0.6, repeat: Infinity, ease: 'linear' }
            : isIdle
            ? { duration: 2, repeat: Infinity }
            : {}
        }
        style={{ transformOrigin: '25px 42px' }}
      >
        <rect x="22" y="42" width="6" height="8" fill="#4a4a5a" />
        <rect x="22" y="50" width="6" height="6" fill="#3a3a4a" />
      </motion.g>

      {/* Legs - Right leg */}
      <motion.g
        animate={
          isWalking
            ? { y: [0, 2, 0, -4, 0], rotate: [0, 4, 0, -8, 0] }
            : isIdle
            ? { rotate: [0, -1, 0] }
            : {}
        }
        transition={
          isWalking
            ? { duration: 0.6, repeat: Infinity, ease: 'linear' }
            : isIdle
            ? { duration: 2, repeat: Infinity }
            : {}
        }
        style={{ transformOrigin: '39px 42px' }}
      >
        <rect x="36" y="42" width="6" height="8" fill="#4a4a5a" />
        <rect x="36" y="50" width="6" height="6" fill="#3a3a4a" />
      </motion.g>

      {/* Body/Torso */}
      <motion.g
        animate={isWalking ? { y: [0, -2, 0, -2, 0] } : {}}
        transition={isWalking ? { duration: 0.6, repeat: Infinity, ease: 'linear' } : {}}
      >
        <rect x="20" y="26" width="24" height="18" fill="#5a5a6a" />
        <rect x="22" y="28" width="4" height="12" fill="#6a6a7a" />
      </motion.g>

      {/* Cape flowing */}
      <motion.g
        animate={
          isWalking
            ? { rotate: [0, 5, 0, -5, 0], y: [0, -2, 0, -2, 0] }
            : { rotate: [0, 3, 0, -3, 0] }
        }
        transition={
          isWalking
            ? { duration: 0.6, repeat: Infinity, ease: 'linear' }
            : { duration: 2.5, repeat: Infinity }
        }
        style={{ transformOrigin: '19px 28px' }}
      >
        <rect x="16" y="28" width="6" height="20" fill="#3a3a4a" opacity="0.8" />
        <rect x="18" y="30" width="4" height="16" fill="#2a2a3a" />
      </motion.g>

      {/* Right arm - raised defensively during parry */}
      <motion.g
        animate={
          isParrying
            ? { rotate: [0, -30, -30, 0], y: [0, -4, -4, 0] }
            : isWalking
            ? { rotate: [0, 10, 0, -10, 0], y: [0, -2, 0, -2, 0] }
            : isIdle
            ? { rotate: [0, -2, 0] }
            : {}
        }
        transition={
          isParrying
            ? {
                duration: 1.6,
                repeat: Infinity,
                times: [0, 0.25, 0.75, 1],
                ease: 'easeInOut',
              }
            : isWalking
            ? { duration: 0.6, repeat: Infinity, ease: 'linear' }
            : isIdle
            ? { duration: 3, repeat: Infinity }
            : {}
        }
        style={{ transformOrigin: '18px 30px' }}
      >
        <rect x="12" y="28" width="6" height="12" fill="#5a5a6a" />
        <rect x="10" y="36" width="4" height="6" fill="#4a4a5a" />
      </motion.g>

      {/* Left arm - raised with sword during parry */}
      <motion.g
        animate={
          isParrying
            ? { rotate: [0, 45, 45, 0], y: [0, -6, -6, 0] }
            : isWalking
            ? { rotate: [0, -10, 0, 10, 0], y: [0, -2, 0, -2, 0] }
            : isIdle
            ? { rotate: [0, 2, 0] }
            : {}
        }
        transition={
          isParrying
            ? {
                duration: 1.6,
                repeat: Infinity,
                times: [0, 0.25, 0.75, 1],
                ease: 'easeInOut',
              }
            : isWalking
            ? { duration: 0.6, repeat: Infinity, ease: 'linear' }
            : isIdle
            ? { duration: 3, repeat: Infinity, delay: 0.5 }
            : {}
        }
        style={{ transformOrigin: '49px 30px' }}
      >
        <rect x="46" y="28" width="6" height="12" fill="#5a5a6a" />
        <rect x="48" y="36" width="6" height="6" fill="#4a4a5a" />
      </motion.g>

      {/* Sword - only visible during parry */}
      {isParrying && (
        <motion.g
          animate={{
            rotate: [0, 45, 45, 0],
            y: [0, -6, -6, 0],
          }}
          transition={{
            duration: 1.6,
            repeat: Infinity,
            times: [0, 0.25, 0.75, 1],
            ease: 'easeInOut',
          }}
          style={{ transformOrigin: '49px 30px' }}
        >
          {/* Sword blade pointing down */}
          <rect x="47" y="8" width="3" height="24" fill="#9aaaba" />
          <rect x="48" y="8" width="1" height="24" fill="#ccdcec" />

          {/* Sword tip */}
          <rect x="48" y="32" width="1" height="2" fill="#8a9aaa" />

          {/* Sword guard/hilt */}
          <rect x="45" y="6" width="7" height="3" fill="#6a6a7a" />
          <rect x="46" y="7" width="5" height="1" fill="#8a8a9a" />

          {/* Handle */}
          <rect x="48" y="2" width="1" height="5" fill="#4a3a2a" />

          {/* Pommel */}
          <rect x="47" y="1" width="3" height="2" fill="#6a6a7a" />

          {/* Sword glow/shine effect */}
          <motion.rect
            x="49"
            y="10"
            width="1"
            height="6"
            fill="#ffffff"
            opacity="0.6"
            animate={{
              opacity: [0, 0.4, 0.8, 0.4, 0],
              y: [10, 10, 20, 20, 10],
            }}
            transition={{
              duration: 1.6,
              repeat: Infinity,
              times: [0, 0.25, 0.5, 0.75, 1],
            }}
          />
        </motion.g>
      )}

      {/* Head */}
      <motion.g
        animate={isWalking ? { y: [0, -2, 0, -2, 0] } : {}}
        transition={isWalking ? { duration: 0.6, repeat: Infinity, ease: 'linear' } : {}}
      >
        <rect x="24" y="14" width="16" height="14" fill="#8a7a6a" />
        <rect x="26" y="16" width="12" height="10" fill="#9a8a7a" />

        {/* Helmet */}
        <rect x="22" y="12" width="20" height="6" fill="#6a6a7a" />
        <rect x="24" y="10" width="16" height="4" fill="#7a7a8a" />

        {/* Face/Eyes */}
        <rect x="28" y="20" width="3" height="3" fill="#2a2a2a" />
        <rect x="37" y="20" width="3" height="3" fill="#2a2a2a" />
      </motion.g>

      {/* Parry energy effect around sword - only during parry */}
      {isParrying && (
        <motion.g
          animate={{
            opacity: [0, 0.4, 0.8, 0.4, 0],
            scale: [0.5, 0.9, 1.1, 0.9, 0.5],
            rotate: [0, 45, 45, 45, 0],
            y: [0, -6, -6, -6, 0],
          }}
          transition={{
            duration: 1.6,
            repeat: Infinity,
            times: [0, 0.25, 0.5, 0.75, 1],
            ease: 'easeInOut',
          }}
          style={{ transformOrigin: '49px 30px' }}
        >
          {/* Energy particles around sword */}
          <rect x="42" y="10" width="2" height="2" fill="#ba9afa" />
          <rect x="40" y="14" width="2" height="2" fill="#ca8afa" />
          <rect x="42" y="18" width="2" height="2" fill="#ba9afa" />
          <rect x="40" y="22" width="2" height="2" fill="#ca8afa" />
          <rect x="42" y="26" width="2" height="2" fill="#ba9afa" />

          <rect x="54" y="12" width="2" height="2" fill="#ba9afa" />
          <rect x="56" y="16" width="2" height="2" fill="#ca8afa" />
          <rect x="54" y="20" width="2" height="2" fill="#ba9afa" />
        </motion.g>
      )}

      {/* Jump swoosh lines */}
      {isJumping && (
        <>
          {/* Motion lines */}
          <motion.g
            animate={{
              opacity: [0, 0.8, 0],
              x: [0, -8, -16],
              y: [0, 3, 6],
            }}
            transition={{
              duration: 0.3,
              repeat: Infinity,
              repeatDelay: 0.3,
            }}
          >
            <rect x="40" y="48" width="12" height="2" fill="#9aaaba" opacity="0.7" />
            <rect x="38" y="52" width="10" height="2" fill="#9aaaba" opacity="0.5" />
            <rect x="36" y="56" width="8" height="2" fill="#9aaaba" opacity="0.3" />
          </motion.g>

          {/* Jump effect particles */}
          <motion.g
            animate={{
              opacity: [0, 0.7, 0],
              y: [0, 8, 16],
              scaleX: [1, 1.2, 1.4],
            }}
            transition={{
              duration: 0.6,
              repeat: Infinity,
            }}
          >
            <rect x="26" y="56" width="3" height="3" fill="#7a8a6a" />
            <rect x="35" y="56" width="3" height="3" fill="#7a8a6a" />
            <rect x="20" y="58" width="2" height="2" fill="#6a7a5a" />
            <rect x="42" y="58" width="2" height="2" fill="#6a7a5a" />
          </motion.g>
        </>
      )}
    </motion.svg>
  );
}

export default function CharacterShowcase() {
  const [selectedState, setSelectedState] = useState<CharacterState>('idle');

  const states: { name: CharacterState; label: string; description: string }[] = [
    { name: 'idle', label: 'Idle Stance', description: 'Breathing animation, ready for action' },
    { name: 'walk', label: 'Walking', description: 'Steady movement with swinging arms' },
    { name: 'jump', label: 'Jump', description: 'Vertical leap with particle effects' },
    { name: 'parry', label: 'Parry', description: 'Sword raised, deflecting projectiles' },
  ];

  return (
    <div
      className="size-full flex items-center justify-center overflow-hidden"
      style={{
        backgroundColor: '#2a3a2e',
        imageRendering: 'pixelated',
      }}
    >
      {/* Main Container */}
      <div className="relative w-full max-w-5xl h-full flex flex-col items-center justify-center px-8 py-12">
        {/* Title */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mb-12 text-center"
        >
          <h1
            className="text-5xl mb-2"
            style={{
              color: '#e0d0b0',
              textShadow: '0 0 20px rgba(186, 154, 250, 0.5)',
              fontFamily: 'monospace',
              letterSpacing: '0.1em',
            }}
          >
            CHARACTER STATES
          </h1>
          <div
            className="h-1 w-64 mx-auto"
            style={{
              background: 'linear-gradient(90deg, transparent, #ba9afa, transparent)',
            }}
          />
        </motion.div>

        {/* Character Display Area */}
        <div className="flex gap-16 items-start justify-center w-full mb-12">
          {/* Large Character Preview */}
          <motion.div
            key={selectedState}
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.4 }}
            className="flex flex-col items-center"
          >
            <div
              className="relative p-12 rounded-lg mb-6"
              style={{
                backgroundColor: 'rgba(42, 58, 46, 0.6)',
                border: '2px solid rgba(186, 154, 250, 0.3)',
                boxShadow: '0 0 40px rgba(186, 154, 250, 0.2)',
              }}
            >
              {/* Atmospheric glow */}
              <div
                className="absolute inset-0 rounded-lg blur-xl opacity-30"
                style={{
                  background: 'radial-gradient(circle, rgba(186, 154, 250, 0.4), transparent 70%)',
                }}
              />

              <CharacterDisplay state={selectedState} />
            </div>

            {/* State Description */}
            <div className="text-center">
              <h2
                className="text-2xl mb-2"
                style={{
                  color: '#ba9afa',
                  fontFamily: 'monospace',
                  letterSpacing: '0.05em',
                }}
              >
                {states.find((s) => s.name === selectedState)?.label}
              </h2>
              <p
                className="text-sm"
                style={{
                  color: '#a0b0a0',
                  fontFamily: 'monospace',
                }}
              >
                {states.find((s) => s.name === selectedState)?.description}
              </p>
            </div>
          </motion.div>

          {/* State Grid */}
          <div className="flex flex-col gap-4">
            {states.map((state, index) => (
              <motion.button
                key={state.name}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1, duration: 0.4 }}
                onClick={() => setSelectedState(state.name)}
                className="flex items-center gap-6 p-4 rounded-lg transition-all"
                style={{
                  backgroundColor:
                    selectedState === state.name
                      ? 'rgba(186, 154, 250, 0.2)'
                      : 'rgba(42, 58, 46, 0.4)',
                  border:
                    selectedState === state.name
                      ? '2px solid rgba(186, 154, 250, 0.6)'
                      : '2px solid rgba(106, 122, 138, 0.3)',
                  cursor: 'pointer',
                  width: '320px',
                }}
              >
                {/* Small preview */}
                <div
                  className="shrink-0"
                  style={{
                    width: '64px',
                    height: '64px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}
                >
                  <CharacterDisplay state={state.name} />
                </div>

                {/* State info */}
                <div className="flex-1 text-left">
                  <div
                    className="font-bold mb-1"
                    style={{
                      color: selectedState === state.name ? '#ba9afa' : '#e0d0b0',
                      fontFamily: 'monospace',
                      fontSize: '14px',
                      letterSpacing: '0.05em',
                    }}
                  >
                    {state.label}
                  </div>
                  <div
                    className="text-xs"
                    style={{
                      color: '#8a9a8a',
                      fontFamily: 'monospace',
                    }}
                  >
                    {state.description}
                  </div>
                </div>
              </motion.button>
            ))}
          </div>
        </div>

        {/* Technical Details */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.6 }}
          className="grid grid-cols-3 gap-6 w-full max-w-3xl"
        >
          {[
            { label: 'RESOLUTION', value: '64×64 px' },
            { label: 'ANIMATION', value: 'Motion Keyframes' },
            { label: 'STYLE', value: 'Pixel Art' },
          ].map((detail, index) => (
            <div
              key={index}
              className="p-4 rounded text-center"
              style={{
                backgroundColor: 'rgba(42, 58, 46, 0.4)',
                border: '1px solid rgba(106, 122, 138, 0.3)',
              }}
            >
              <div
                className="text-xs mb-1"
                style={{
                  color: '#6a7a8a',
                  fontFamily: 'monospace',
                  letterSpacing: '0.1em',
                }}
              >
                {detail.label}
              </div>
              <div
                className="font-bold"
                style={{
                  color: '#e0d0b0',
                  fontFamily: 'monospace',
                  fontSize: '16px',
                }}
              >
                {detail.value}
              </div>
            </div>
          ))}
        </motion.div>

        {/* Back button */}
        <motion.a
          href="/"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="mt-12 px-6 py-3 rounded"
          style={{
            backgroundColor: 'rgba(106, 122, 138, 0.3)',
            border: '2px solid rgba(186, 154, 250, 0.4)',
            color: '#ba9afa',
            fontFamily: 'monospace',
            fontSize: '14px',
            letterSpacing: '0.1em',
            textDecoration: 'none',
            transition: 'all 0.2s',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.backgroundColor = 'rgba(186, 154, 250, 0.2)';
            e.currentTarget.style.borderColor = 'rgba(186, 154, 250, 0.8)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = 'rgba(106, 122, 138, 0.3)';
            e.currentTarget.style.borderColor = 'rgba(186, 154, 250, 0.4)';
          }}
        >
          ← BACK TO MENU
        </motion.a>
      </div>

      {/* Atmospheric lighting overlay */}
      <div className="absolute inset-0 pointer-events-none mix-blend-multiply">
        <div
          className="absolute w-96 h-96 rounded-full blur-3xl"
          style={{
            top: '20%',
            left: '15%',
            background: 'radial-gradient(circle, rgba(200, 160, 80, 0.2), transparent 70%)',
          }}
        />
        <div
          className="absolute w-96 h-96 rounded-full blur-3xl"
          style={{
            top: '50%',
            right: '20%',
            background: 'radial-gradient(circle, rgba(186, 154, 250, 0.15), transparent 70%)',
          }}
        />
      </div>

      {/* Vignette */}
      <div className="absolute inset-0 pointer-events-none bg-gradient-radial from-transparent via-transparent to-black/60" />

      {/* Pixel grid overlay */}
      <div
        className="absolute inset-0 pointer-events-none opacity-[0.02]"
        style={{
          backgroundImage: `
            repeating-linear-gradient(0deg, transparent, transparent 7px, #000 7px, #000 8px),
            repeating-linear-gradient(90deg, transparent, transparent 7px, #000 7px, #000 8px)
          `,
        }}
      />
    </div>
  );
}
