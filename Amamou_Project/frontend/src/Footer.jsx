import React from 'react'
import {
  FaGithub,
  FaInstagram,
  FaFacebookF,
  FaWhatsapp,
  FaLinkedin
} from 'react-icons/fa'

function Footer() {
  return (
    <footer className="footer">
      <div className="social-icons">
        <a href="https://www.instagram.com/yassir_tage/" target="_blank"><FaInstagram/></a>
        <a href="https://wa.me/+212675630026" target="_blank"><FaWhatsapp/></a>
        <a href="https://www.linkedin.com/in/yassir-tagemouati-471a6a2a2/" target="_blank"><FaLinkedin/></a>
        <a href="https://github.com/TageYassir" target="_blank"><FaGithub/></a>
      </div>
      <p className="copyright">© {new Date().getFullYear()} All rights reserved.</p>
    </footer>
  )
}

export default Footer
