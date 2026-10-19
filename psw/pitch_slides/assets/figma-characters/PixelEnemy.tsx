import { motion } from 'motion/react';

export function PixelEnemy() {
  return (
    <motion.svg
      width="48"
      height="56"
      viewBox="0 0 48 56"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      style={{ imageRendering: 'pixelated' }}
      animate={{
        y: [0, -4, 0],
      }}
      transition={{
        duration: 2,
        repeat: Infinity,
        ease: "easeInOut"
      }}
    >
      {/* Shadow */}
      <ellipse cx="24" cy="52" rx="14" ry="4" fill="#000000" opacity="0.5" />
      
      {/* Body - blob-like creature */}
      <g>
        {/* Base body */}
        <rect x="10" y="28" width="28" height="20" fill="#3a4a3a" />
        <rect x="8" y="30" width="32" height="16" fill="#4a5a4a" />
        <rect x="12" y="32" width="24" height="12" fill="#5a6a5a" />
        
        {/* Body shading */}
        <rect x="14" y="34" width="4" height="8" fill="#6a7a6a" opacity="0.6" />
        <rect x="30" y="36" width="4" height="6" fill="#3a4a3a" opacity="0.7" />
        
        {/* Moss/slime texture */}
        <rect x="16" y="38" width="2" height="2" fill="#4a6a4a" opacity="0.8" />
        <rect x="26" y="40" width="2" height="2" fill="#4a6a4a" opacity="0.8" />
        <rect x="20" y="42" width="2" height="2" fill="#5a7a5a" opacity="0.7" />
      </g>
      
      {/* Head/Top section */}
      <g>
        <rect x="14" y="18" width="20" height="12" fill="#4a5a4a" />
        <rect x="12" y="20" width="24" height="8" fill="#5a6a5a" />
        <rect x="16" y="22" width="16" height="6" fill="#6a7a6a" />
        
        {/* Head highlight */}
        <rect x="18" y="23" width="4" height="4" fill="#7a8a7a" opacity="0.5" />
      </g>
      
      {/* Eyes - glowing menacing */}
      <motion.g
        animate={{
          opacity: [1, 0.6, 1],
        }}
        transition={{
          duration: 3,
          repeat: Infinity,
        }}
      >
        <rect x="18" y="24" width="4" height="4" fill="#8a4a4a" />
        <rect x="19" y="25" width="2" height="2" fill="#ca6a6a" />
        
        <rect x="26" y="24" width="4" height="4" fill="#8a4a4a" />
        <rect x="27" y="25" width="2" height="2" fill="#ca6a6a" />
      </motion.g>
      
      {/* Tentacles/appendages */}
      <g>
        {/* Left tentacle */}
        <rect x="6" y="36" width="6" height="8" fill="#3a4a3a" />
        <rect x="4" y="38" width="4" height="6" fill="#2a3a2a" />
        <rect x="6" y="40" width="2" height="2" fill="#4a5a4a" />
        
        {/* Right tentacle */}
        <rect x="36" y="36" width="6" height="8" fill="#3a4a3a" />
        <rect x="40" y="38" width="4" height="6" fill="#2a3a2a" />
        <rect x="38" y="40" width="2" height="2" fill="#4a5a4a" />
      </g>
      
      {/* Bottom tendrils touching ground */}
      <g opacity="0.8">
        <rect x="14" y="48" width="3" height="4" fill="#2a3a2a" />
        <rect x="20" y="48" width="3" height="4" fill="#2a3a2a" />
        <rect x="25" y="48" width="3" height="4" fill="#2a3a2a" />
        <rect x="31" y="48" width="3" height="4" fill="#2a3a2a" />
      </g>
      
      {/* Dripping slime effect */}
      <motion.g
        animate={{
          y: [0, 4],
          opacity: [0.8, 0],
        }}
        transition={{
          duration: 1.5,
          repeat: Infinity,
        }}
      >
        <rect x="22" y="48" width="2" height="2" fill="#4a6a4a" />
        <rect x="23" y="50" width="2" height="2" fill="#5a7a5a" />
      </motion.g>
      
      {/* Ambient glow - menacing aura */}
      <motion.rect
        x="8"
        y="20"
        width="32"
        height="28"
        fill="#8a4a4a"
        opacity="0.15"
        animate={{
          opacity: [0.1, 0.2, 0.1],
          scale: [1, 1.05, 1],
        }}
        transition={{
          duration: 2.5,
          repeat: Infinity,
        }}
      />
      
      {/* Energy particles around enemy */}
      <motion.rect
        x="8"
        y="26"
        width="2"
        height="2"
        fill="#6a4a4a"
        animate={{
          x: [8, 4],
          y: [26, 22],
          opacity: [0.7, 0],
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          delay: 0.5,
        }}
      />
      
      <motion.rect
        x="38"
        y="30"
        width="2"
        height="2"
        fill="#6a4a4a"
        animate={{
          x: [38, 42],
          y: [30, 26],
          opacity: [0.7, 0],
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          delay: 1,
        }}
      />
    </motion.svg>
  );
}
