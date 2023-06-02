from flask import Blueprint, request, render_template, session, redirect, flash
import hashlib, base64, json

user_bp = Blueprint('user_bp', __name__)